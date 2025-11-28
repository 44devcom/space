#!/bin/bash
set -e

echo "=== SPACE CREATE WIZARD AGENT ==="

# Get project description from environment or arguments
PROJECT_DESC="${SPACE_PROJECT_DESC:-$1}"

if [ -z "$PROJECT_DESC" ]; then
  echo "Error: Project description required."
  echo "Usage: SPACE_PROJECT_DESC='<description>' ./run-create-wizard-agent.sh"
  echo "   or: ./run-create-wizard-agent.sh '<description>'"
  exit 1
fi

echo "Project description: $PROJECT_DESC"
echo ""

# Step 1: Call create-plan-agent
echo "Step 1: Creating project plan..."
export SPACE_PROJECT_DESC="$PROJECT_DESC"
node cursor-agent.js run create-plan-agent || {
  echo "Error: Failed to create plan"
  exit 1
}

# Step 2: Find the generated plan file
# Plans are saved as .cursor/plans/<project-id>.plan.json
# We'll need to find the most recently created plan
PLAN_DIR=".cursor/plans"
if [ ! -d "$PLAN_DIR" ]; then
  echo "Error: Plan directory not found: $PLAN_DIR"
  exit 1
fi

# Get the most recently modified plan file
PLAN_FILE=$(find "$PLAN_DIR" -name "*.plan.json" -type f -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)

if [ -z "$PLAN_FILE" ] || [ ! -f "$PLAN_FILE" ]; then
  echo "Error: No plan file found in $PLAN_DIR"
  exit 1
fi

echo "Plan file: $PLAN_FILE"
echo ""

# Step 3: Extract project ID from plan file
PROJECT_ID=$(basename "$PLAN_FILE" .plan.json)
echo "Project ID: $PROJECT_ID"
echo ""

# Step 4: Print plan overview
echo "=== PLAN OVERVIEW ==="
if command -v jq &> /dev/null; then
  echo "Milestones:"
  jq -r '.milestones[] | "  - \(.title) (id: \(.id))"' "$PLAN_FILE" || true
  echo ""
  echo "Issues:"
  jq -r '.milestones[].issues[]? | "  - \(.title) (id: \(.id))"' "$PLAN_FILE" || true
  echo ""
  echo "Task types:"
  jq -r '.milestones[].issues[].tasks[]?.type // empty' "$PLAN_FILE" | sort -u | sed 's/^/  - /' || true
else
  echo "Install 'jq' for detailed plan overview"
  echo "Plan saved to: $PLAN_FILE"
fi
echo ""

# Step 5: Execute plan with --dry preview
echo "=== DRY RUN PREVIEW ==="
export SPACE_PROJECT_ID="$PROJECT_ID"
node cursor-agent.js run run-plan-agent --dry || {
  echo "Warning: Dry run failed, but continuing..."
}
echo ""

# Step 6: Execute plan (final run)
echo "=== EXECUTING PLAN ==="
read -p "Proceed with execution? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  export SPACE_PROJECT_ID="$PROJECT_ID"
  node cursor-agent.js run run-plan-agent || {
    echo "Error: Plan execution failed"
    exit 1
  }
  echo ""
  echo "=== WIZARD COMPLETE ==="
  echo "Plan executed successfully!"
else
  echo "Execution cancelled. Plan saved to: $PLAN_FILE"
  echo "Run manually with: node cursor-agent.js run run-plan-agent"
fi

