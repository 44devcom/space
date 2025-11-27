# Create MVC Agent

## Purpose
Produce a full MVC scaffold for any Entity across:
- Laravel
- Express/TypeScript
- FastAPI/Python

## Steps
1. Resolve stack via Worktree Resolver
2. Generate MVC Model via create-mvc-model-agent
3. Generate MVC Controller via create-mvc-controller-agent
4. Generate MVC Views via create-mvc-view-agent
5. Generate BDD Feature tests
6. Generate TDD Unit tests

## Inputs
- Entity name
- Optional: field definitions

## Outputs
Written to:
- mvc.models
- mvc.controllers
- mvc.views
- tests.bdd
- tests.unit