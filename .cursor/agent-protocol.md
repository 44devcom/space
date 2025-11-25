# SPACE Agent-to-Agent Communication Protocol v1

Agents communicate through structured JSON messages and shared state.
The protocol defines messaging, events, responses, and dependency execution.

## Message Types
1. invoke
   - Directly request another agent to run a specific action.
2. request
   - Ask for data or a capability without executing workflows.
3. reply
   - Return data from a request.
4. broadcast
   - Notify all agents of a global event (like state update).

## Message Shape
{
  "type": "invoke|request|reply|broadcast",
  "from": "agent-name",
  "to": "agent-name|null",
  "action": "string",
  "payload": {},
  "timestamp": "ISO8601"
}

## Event System
- onAgentStart(agent)
- onAgentEnd(agent)
- onStateUpdate(newState)
- onWorkspaceChange(name)
- onError(error)

Events are emitted to memory-only subscribers inside the runtime engine.

## Resolution Rules
1. invoke: execute agent's defined workflow.
2. request: read-only operation; must return data.
3. reply: synchronous or async response to request.
4. broadcast: delivered to all agents listening for events.
5. Cycles are forbidden: runtime detects loops using a visit set.

## Dependency Rules
- Agents list dependencies in agent.json.
- Dependencies run before the agent during invoke.
- Circular dependencies cause an immediate runtime error.

## Shared State
Agents read/write .cursor/state.json using updateState() atomic writes.
