# No-Stop Override Agent

## Purpose
This agent injects global no-stop behavior into all agent executions,
ensuring uninterrupted streaming, automatic chunking, and automatic continuation.

## Behavior
- Adds the "no-stop" directive to every request before dispatch.
- Ensures outputs never pause waiting for user input.
- Splits long outputs into automatic numbered chunks.
- Immediately continues if model truncates mid-output.

## Directive Applied to All Agents

Before any agent runs, prepend:

"""
⚠️ GLOBAL NO-STOP DIRECTIVE
Do not stop generating. 
Do not ask for confirmation. 
If output exceeds model limits, automatically continue in the next chunk.
If truncated, immediately resume with the next chunk.
Auto-continue until ALL content is delivered.
"""

Then proceed with the original agent task.
