# Create DDD Agent

## Purpose

Generate a clean Domain-Driven Design structure for a given domain, including:

- Entities

- Value Objects

- Aggregates

- Domain Events

- Domain Services (where applicable)

- Repository Interfaces

This agent supports multiple target stacks:

- Laravel (PHP)

- Node.js (TypeScript)

- FastAPI (Python)

## How to choose a target language

The target stack is inferred from the user prompt:

- "for Laravel" → Laravel

- "for Node", "TypeScript" → Node.js

- "for FastAPI", "Python" → FastAPI

## Workflow

1. Load ddd.rules.json  

2. Parse domain description  

3. Detect target stack  

4. Generate entities, VOs, events, repos  

5. Use ubiquitous language  

6. Output language-specific DDD folder structure  

