// .cursor/event-bus.js

/**
 * SPACE Agent Event Bus v1
 *
 * Simple synchronous pub/sub bus with optional agent listener runner.
 * - eventBus.on(eventName, handler)
 * - eventBus.off(eventName, handler)
 * - eventBus.emit(eventName, payload)
 * - eventBus.setAgentListenerRunner(fn)
 */

const listeners = {};
let agentListenerRunner = null;

function on(eventName, handler) {
  if (!listeners[eventName]) {
    listeners[eventName] = new Set();
  }
  listeners[eventName].add(handler);
}

function off(eventName, handler) {
  if (!listeners[eventName]) return;
  listeners[eventName].delete(handler);
  if (listeners[eventName].size === 0) {
    delete listeners[eventName];
  }
}

function setAgentListenerRunner(fn) {
  agentListenerRunner = fn;
}

function emit(eventName, payload) {
  // Local JS listeners
  const handlers = listeners[eventName];
  if (handlers) {
    for (const handler of handlers) {
      try {
        handler(payload, eventName);
      } catch (err) {
        // Don't break the bus if one handler fails
        // eslint-disable-next-line no-console
        console.error("[event-bus][handler-error]", eventName, err.message);
      }
    }
  }

  // Listener agents (optional)
  if (typeof agentListenerRunner === "function") {
    try {
      agentListenerRunner(eventName, payload);
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error("[event-bus][agent-listener-error]", eventName, err.message);
    }
  }
}

module.exports = {
  on,
  off,
  emit,
  setAgentListenerRunner
};
