#!/bin/bash
set -e

# ==========================================
# SPACE /git-push runner
# Usage: ./git-push-runner.sh <token>
# ==========================================

TOKEN="$1"

if [ -z "$TOKEN" ]; then
  echo "ERROR: Missing GitHub token."
  echo "Usage: ./git-push-runner.sh <token>"
  exit 1
fi

# ==========================================
# Step 1: Ensure SSH keys exist
# ==========================================

SSH_DIR="$HOME/.ssh"
KEY_PATH="$SSH_DIR/id_ed25519"

if [ ! -f "$KEY_PATH" ]; then
  echo "[git-push] No SSH key found. Generating new ED25519 key..."
  mkdir -p "$SSH_DIR"
  ssh-keygen -t ed25519 -C "space-runtime" -f "$KEY_PATH" -N ""
else
  echo "[git-push] SSH key already exists: $KEY_PATH"
fi

# Start ssh-agent if not running
if [ -z "$SSH_AUTH_SOCK" ]; then
  echo "[git-push] Starting ssh-agent..."
  eval "$(ssh-agent -s)"
fi

# Add key to agent
ssh-add "$KEY_PATH"

# ==========================================
# Step 2: Extract GitHub owner/repo
# ==========================================

ORIGIN_URL=$(git remote get-url origin 2>/dev/null || true)

if [ -z "$ORIGIN_URL" ]; then
  echo "ERROR: No 'origin' remote found. Add one first:"
  echo "git remote add origin git@github.com:<owner>/<repo>.git"
  exit 1
fi

# Expect format: git@github.com:<owner>/<repo>.git
if [[ "$ORIGIN_URL" =~ git@github.com:(.*)/(.*)\.git ]]; then
  OWNER="${BASH_REMATCH[1]}"
  REPO="${BASH_REMATCH[2]}"
else
  echo "ERROR: Remote origin is not in SSH format:"
  echo "       $ORIGIN_URL"
  echo "Expected: git@github.com:<owner>/<repo>.git"
  exit 1
fi

echo "[git-push] Detected repository: $OWNER/$REPO"

# ==========================================
# Step 3: Upload PUBLIC key to GitHub as Deploy Key
# (Token is used temporarily, not saved)
# ==========================================

PUB_KEY=$(cat "$KEY_PATH.pub")

echo "[git-push] Uploading public key as GitHub Deploy Key..."

UPLOAD_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/$OWNER/$REPO/keys \
  -d "{
        \"title\": \"SPACE Deploy Key\",
        \"key\": \"$PUB_KEY\",
        \"read_only\": false
      }"
)

# Remove token from memory securely by overwriting bash var
TOKEN="###########"
unset TOKEN

if [ "$UPLOAD_RESPONSE" = "201" ] || [ "$UPLOAD_RESPONSE" = "422" ]; then
  # 422 = key already exists (safe to continue)
  echo "[git-push] Deploy key uploaded (or already exists)."
else
  echo "ERROR: Failed to upload deploy key. HTTP status: $UPLOAD_RESPONSE"
  echo "Possible causes:"
  echo "- Token missing 'repo' permissions"
  echo "- Repo is private and token does not have access"
  exit 1
fi

# ==========================================
# Step 4: Ensure the remote uses SSH format
# ==========================================

git remote set-url origin "git@github.com:$OWNER/$REPO.git"
echo "[git-push] Ensured SSH remote format."

# ==========================================
# Step 5: Push to GitHub
# ==========================================

CURRENT_BRANCH=$(git branch --show-current)

echo "[git-push] Pushing branch: $CURRENT_BRANCH"

# First try normal push
if git push; then
  echo "[git-push] Push successful."
  exit 0
fi

# If upstream missing, set it
echo "[git-push] No upstream branch set. Setting upstream..."
git push --set-upstream origin "$CURRENT_BRANCH"

echo "[git-push] Push complete."
