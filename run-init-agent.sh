#!/bin/bash
set -e

echo "=== SPACE INIT AGENT ==="

# 1. Create core directories
echo "Creating directories..."
mkdir -p .github/workflows
mkdir -p tasks
mkdir -p .cursor

# 2. Ensure README exists
if [ ! -f README.md ]; then
  echo "Creating README.md..."
  cat > README.md <<'EOF'
# SPACE

Portable workspace manager.

## DEVELOPMENT

On-demand, agile development.

### README.md

Primary source of truth. All other parts must be iterated from this.

### CHANGELOG.md

Chronological record of updates, improvements, and breaking changes.
EOF
fi

# 3. Ensure CHANGELOG exists
if [ ! -f CHANGELOG.md ]; then
  echo "Creating CHANGELOG.md..."
  cat > CHANGELOG.md <<'EOF'
# Changelog
All notable changes to this project will be documented in this file.

The format is based on https://keepachangelog.com/en/1.1.0/
and this project adheres to Semantic Versioning.

## [Unreleased]
### Added
- Initial project structure.

EOF
fi

# 4. Place workflow files if missing
if [ ! -f .github/workflows/release.yml ]; then
  echo "Installing release.yml workflow..."
  cat > .github/workflows/release.yml <<'EOF'
name: Release

on:
  push:
    branches:
      - main
      - master

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - name: Release Please
        uses: google-github-actions/release-please-action@v4
        with:
          release-type: simple
          package-name: space
EOF
fi

if [ ! -f .github/workflows/update-changelog.yml ]; then
  echo "Installing update-changelog.yml workflow..."
  cat > .github/workflows/update-changelog.yml <<'EOF'
name: Update Changelog

on:
  pull_request:
    types: [closed]

permissions:
  contents: write
  pull-requests: write

jobs:
  update:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Append PR entry to Unreleased section
        run: |
          sed -i "/## \[Unreleased\]/a - Merged PR #${{ github.event.pull_request.number }}: ${{ github.event.pull_request.title }}" CHANGELOG.md

      - name: Commit changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "docs: update changelog for PR #${{ github.event.pull_request.number }}"
EOF
fi

# 5. Initialize Git if not present
if [ ! -d .git ]; then
  echo "Initializing git repository..."
  git init
  git branch -M master
  git add .
  git commit -m "feat: initialize SPACE ecosystem"
else
  echo "Git already initialized."
fi

# 6. Create workspace file in .cursor/
if [ ! -f .cursor/workspace.json ]; then
  echo "Creating workspace definition in .cursor/workspace.json..."
  cat > .cursor/workspace.json <<EOF
{
  "name": "$(basename "$PWD")",
  "branch": "$(git branch --show-current || echo master)",
  "created": "$(date -Iseconds)",
  "env": {},
  "tools": []
}
EOF
fi

echo "=== INIT COMPLETE ==="
