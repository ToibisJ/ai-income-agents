# Architecture

## Agent Roles

### Strategist (claude-opus-4-8)
- Reads shared state
- Decides the next best action
- Evaluates Executor's results
- Updates strategy

### Executor (claude-sonnet-4-6)
- Receives instructions from Strategist
- Takes action (or reports what action needs to be taken manually)
- Reports results back

### Coordinator (coordinator.py)
- Runs the session loop
- Passes messages between agents
- Saves state and writes journal

## Communication Flow

```
Strategist → [instruction] → Executor → [result] → Strategist → [evaluation] → State
```

Each full cycle = one session. Sessions are logged to /journal/.

## Memory (shared_state.json)

All agents read and write from this single file.
This is the source of truth for:
- Budget tracking
- Active projects
- Decisions log
- Notes from each agent

## Extensibility

To add a new tool:
1. Create `tools/your_tool.py`
2. Import in `executor.py`
3. Add to the Executor's system prompt
