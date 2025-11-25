# Push

Push the current Git branch to GitHub using **SSH authentication**.  
Automatically handles SSH key creation, deploy key upload, remote normalization, and upstream configuration.

This command uses a **one-time GitHub token** to upload the SSH public key as a **Deploy Key with write access**.  
The token is **never stored**, **never written**, **never logged**, and is **deleted from memory immediately** after the upload.

---

## Usage

```bash
/git-push <token>
```

### Parameters

**<token>**  
A GitHub Personal Access Token (PAT), GitHub App installation token, or temporary GitHub token with:

- `repo` → write access

The token is only used for the deploy key upload step and then immediately forgotten.

---

## Behavior Overview

1. **Validate Token**
   - If `<token>` is missing → abort.

2. **Ensure SSH key exists**
   - Expected path: `~/.ssh/id_ed25519`
   - If missing:
     ```bash
     ssh-keygen -t ed25519 -C "space-runtime" -f ~/.ssh/id_ed25519 -N ""
     ```
   - Ensure ssh-agent is running and key is loaded:
     ```bash
     eval "$(ssh-agent -s)"
     ssh-add ~/.ssh/id_ed25519
     ```

3. **Extract repository owner/repo**
   From:
   ```bash
   git remote get-url origin
   ```
   Expected format:
   ```bash
   git@github.com:<owner>/<repo>.git
   ```

4. **Upload the *public* key to GitHub**
   Using the provided token (never stored):
   ```bash
   curl -X POST \
     -H "Authorization: token <token>" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/repos/<owner>/<repo>/keys \
     -d '{
       "title": "SPACE Deploy Key",
       "key": "<CONTENT OF ~/.ssh/id_ed25519.pub>",
       "read_only": false
     }'
   ```

**Important:**
- Only the **public** key is uploaded.
- The **private** key never leaves the machine.
- A 422 response (“already exists”) is safe and means it’s reusable.

5. **Token is destroyed**
   After the curl request:
   ```bash
   unset TOKEN
   TOKEN="###########"
   ```
   Token is forgotten forever.

6. **Ensure SSH remote format**
   For consistency:
   ```bash
   git remote set-url origin git@github.com:<owner>/<repo>.git
   ```

7. **Push branch**
- First attempt:
  ```
  git push
  ```
- If upstream missing:
  ```
  git push --set-upstream origin <current-branch>
  ```

8. **Confirm**
   ```bash
   git status
   ```

---

## Runner Script

This command uses the following runner:

```bash
./git-push-runner.sh <token>
```

Which implements the full push flow.

---

## Notes

- Only **SSH authentication** is used (never HTTPS).  
- The deploy key allows **write operations**, enabling CI or agents.  
- Token is **not saved**, **not printed**, **not logged**, and **not written to disk**.  
- Safe to call repeatedly.  
- Will not upload multiple keys if one already exists.

---

## Example

```bash
/git-push ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXX # token used once
```

---

This upgraded `/git-push` command is now fully aligned with the SPACE ecosystem, the Cursor agent runtime, and the secure deploy-key model.