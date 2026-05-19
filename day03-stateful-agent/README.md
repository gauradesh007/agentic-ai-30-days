# Day 3 — Stateful Retry Agent

## Objective

Day 3 focused on making the agent stateful and more reliable by adding:

- state tracking
- failure history
- retry counts
- observation memory
- stopping conditions
- incomplete-task reporting

The goal was to move beyond simple tool routing and begin building agents that can remember what happened during execution.

---

## Core Lesson

A useful agent does not just call tools.

A reliable agent must remember:

- what tools were already used
- which tool calls succeeded
- which tool calls failed
- how many times a failure happened
- when to stop trying

Key insight:

State turns a tool-using script into a workflow-aware agent.

---

## Tools Used

| Tool | Purpose |
|---|---|
| current_date | Gets the real system date |
| calculator | Performs math calculations |

---

## Agent State

The agent tracks state using:

tool_results = {}
failure_history = []
retry_count = {}

### tool_results

Stores successful tool outputs.

Example:

{
    "current_date": "Monday, 18 May 2026",
    "calculator": "1364.0"
}

### failure_history

Stores failed tool attempts.

Example:

[
    {
        "tool": "calculator",
        "input": "twenty two percent of 6200",
        "error": "ERROR: Invalid expression"
    }
]

### retry_count

Tracks how many times a tool failed.

Example:

{
    "calculator": 1
}

---

## Example Successful Run

Question:

What day is it today and what is 22% of 6200?

Final controller answer:

Today is Monday, 18 May 2026.
22% of 6200 is 1364.0.

---

## Failure Testing

The agent was tested with harder input:

What day is it today and what is twenty two percent of 6200?

This caused the calculator tool to fail because the input was not a valid math expression.

The agent correctly recorded:

- failed tool name
- failed input
- error message
- retry count

This showed that the agent can track failures instead of pretending the task succeeded.

---

## Why This Matters

Real agent systems must handle failure.

Models can:

- hallucinate
- produce invalid inputs
- repeat bad actions
- generate malformed JSON
- invent answers

The controller must protect the workflow by tracking state and failures.

---

## Architecture

User Question
   ↓
Model Suggests Action
   ↓
Controller Validates Action
   ↓
Tool Executes
   ↓
Success or Failure Detected
   ↓
State Updated
   ↓
Retry Logic Applied
   ↓
Final State Reported

---

## Key Concepts Learned

- Agent state
- Failure history
- Retry logic
- Tool result tracking
- Workflow stopping conditions
- Honest incomplete-task reporting
- Difference between happy-path testing and failure-path testing

---

## Most Important Insight

Happy-path demos are not enough.

Reliable agents must be tested against failure paths.

---

## Technologies Used

- Python
- Ollama
- llama3.2:1b
- requests
- local tool execution
- JSON extraction
- state tracking

---

## Future Improvements

Possible next improvements:

- automatic correction of natural-language math
- smarter retry strategies
- dynamic tool requirement detection
- persistent memory
- structured logs
- ReAct-style reasoning traces
- LangGraph-based workflow version
