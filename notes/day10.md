# Day 10 Notes — Self-Correcting Agent

# Overview

Day 10 focused on building a self-correcting AI workflow agent capable of:

- detecting failed tool executions
- generating correction recommendations
- retrying failed actions automatically
- maintaining correction history
- maintaining retry history
- combining reflection and correction
- performing primitive self-healing
- recovering from workflow failures

The goal was to move beyond passive reflection systems and begin building workflows that can recover from their own mistakes.

---

# Core Lesson

Reflection alone is not enough.

A reliable AI workflow system should:

- perform actions
- inspect observations
- generate reflections
- identify failures
- generate corrections
- retry improved actions

The Day 10 workflow introduced:

```text
self-correcting workflow orchestration
```

This became a major architectural step toward:

- self-healing agents
- adaptive systems
- autonomous workflows
- self-improving AI architectures

---

# Day 10 Workflow Architecture

```text
User Question
      ↓
Memory Retrieval
      ↓
Relevant Context
      ↓
Tool Selection
      ↓
Controller Validation
      ↓
Tool Execution
      ↓
Observation
      ↓
Reflection
      ↓
Correction
      ↓
Retry
      ↓
Final Summary
```

This architecture introduced active recovery into the workflow lifecycle.

---

# Reflection + Correction Architecture

Day 10 extended Day 9's reflection system.

Day 9:

```text
Thought
↓
Action
↓
Observation
↓
Reflection
```

Day 10:

```text
Thought
↓
Action
↓
Observation
↓
Reflection
↓
Correction
↓
Retry
```

This introduced the first form of:

```text
workflow self-healing
```

---

# Correction State

Day 10 introduced:

```python
correction_history = []
```

Example:

```python
correction_history = [
    "Use decimal multiplication instead of natural language."
]
```

Purpose:

- record correction recommendations
- explain recovery decisions
- support workflow debugging
- document self-healing behavior

---

# Retry State

Day 10 introduced:

```python
retry_history = []
```

Example:

```python
retry_history = [
    {
        "tool": "calculator",
        "corrected_input": "0.15 * 5000"
    }
]
```

Purpose:

- track retry attempts
- document recovery actions
- inspect workflow corrections
- support execution auditing

---

# Correction Function

The workflow introduced:

```python
generate_correction()
```

Example:

```python
def generate_correction(tool_name, result):

    if not result.startswith("ERROR"):
        return None

    if tool_name == "calculator":
        return (
            "Use decimal multiplication "
            "instead of natural language."
        )
```

This allowed the workflow to generate recovery suggestions.

---

# Retry Function

The workflow introduced:

```python
retry_with_correction()
```

Example:

```python
def retry_with_correction(tool_name, correction):

    if tool_name == "calculator":
        return "0.15 * 5000"
```

This converted correction suggestions into executable inputs.

---

# Tools Used

## current_date

Purpose:
- retrieve actual system date

Used because local models frequently hallucinated dates.

Example output:

```text
Sunday, 31 May 2026
```

---

## calculator

Purpose:
- execute mathematical calculations

Example:

```python
calculator("0.15 * 5000")
```

Output:

```text
750.0
```

---

## text_length

Purpose:
- count characters in text

Example:

```python
text_length("Agentic")
```

Output:

```text
7
```

---

# Retrieval-Aware Foundation

Day 10 continued using the Day 8 retrieval architecture.

Example retrieved memory:

```text
Percentage calculations should use decimal multiplication.
current_date tool returns the real system date.
text_length counts characters in a string.
```

This memory continued supporting:

- tool selection
- fallback logic
- reflection
- correction generation

---

# Agent State

The Day 10 workflow maintained multiple workflow states.

## tool_results

Stores successful tool outputs.

Example:

```python
tool_results = {
    "current_date": "Sunday, 31 May 2026",
    "calculator": "750.0",
    "text_length": "7"
}
```

Purpose:

- preserve observations
- track completed tools
- support final summary generation

---

## thought_history

Stores workflow reasoning.

Example:

```python
thought_history = [
    "What day is it today?",
    "Retrieved memory says percentage calculations should use decimal multiplication."
]
```

Purpose:

- inspect workflow reasoning
- analyze decisions
- debug execution

---

## reflection_history

Stores workflow evaluations.

Example:

```python
reflection_history = [
    "current_date completed successfully. Result appears valid.",
    "calculator failed. The workflow may require correction."
]
```

Purpose:

- evaluate outcomes
- inspect workflow quality
- improve observability

---

## correction_history

Stores recovery suggestions.

Example:

```python
correction_history = [
    "Use decimal multiplication instead of natural language."
]
```

Purpose:

- document recovery reasoning
- explain retry decisions

---

## retry_history

Stores retry actions.

Example:

```python
retry_history = [
    {
        "tool": "calculator",
        "corrected_input": "0.15 * 5000"
    }
]
```

Purpose:

- track self-healing actions
- inspect recovery behavior

---

# Self-Correcting Workflow

The workflow became:

```text
Memory Retrieval
↓
Reasoning
↓
Action
↓
Observation
↓
Reflection
↓
Correction
↓
Retry
↓
Final Result
```

This is much closer to:

- autonomous agents
- adaptive workflows
- self-healing systems
- production AI orchestration

---

# Example Workflow

## Step 1

Tool:

```text
current_date
```

Observation:

```text
Sunday, 31 May 2026
```

Reflection:

```text
current_date completed successfully. Result appears valid.
```

No correction required.

---

## Step 2

Tool:

```text
calculator
```

Input:

```text
fifteen percent of 5000
```

Observation:

```text
ERROR: Invalid expression
```

Reflection:

```text
calculator failed. The workflow may require correction.
```

Correction:

```text
Use decimal multiplication instead of natural language.
```

Retry Input:

```text
0.15 * 5000
```

Retry Result:

```text
750.0
```

This demonstrated true self-correction.

---

## Step 3

Tool:

```text
text_length
```

Input:

```text
Agentic
```

Observation:

```text
7
```

Reflection:

```text
text_length completed successfully. Result appears valid.
```

No correction required.

---

# Self-Healing Behavior

One of the biggest Day 10 improvements was:

```text
The workflow no longer stopped after failure.
```

Instead:

```text
Failure
↓
Reflection
↓
Correction
↓
Retry
↓
Success
```

This became the first form of:

```text
self-healing execution
```

---

# Problems Observed

The local model continued producing:

- incorrect dates
- repeated completed tools
- invalid calculator inputs
- contradictory reasoning
- malformed workflow suggestions

Example:

```text
15, 5000
```

instead of:

```text
0.15 * 5000
```

The controller corrected execution and the retry system recovered successfully.

---

# Controller Responsibilities

The controller remained responsible for:

- validating tool selection
- preventing repeated tools
- enforcing workflow order
- correcting invalid model behavior
- maintaining workflow reliability

The controller remained the reliability layer.

---

# Reflection vs Correction

A very important Day 10 distinction emerged.

## Reflection

Reflection asks:

```text
What happened?
```

Example:

```text
calculator failed.
```

---

## Correction

Correction asks:

```text
What should we do next?
```

Example:

```text
Use decimal multiplication instead of natural language.
```

This distinction is foundational for autonomous systems.

---

# Key Concepts Learned

- self-correcting workflows
- correction history
- retry systems
- workflow recovery
- self-healing execution
- reflection-driven recovery
- controller-guided correction
- primitive autonomous recovery

---

# Most Important Insights

## 1. Reflection alone is passive

Reflection identifies problems.

It does not solve them.

---

## 2. Correction creates recovery

Correction converts:

```text
failure
```

into:

```text
improved retry
```

This is the beginning of self-healing systems.

---

## 3. Controllers still remain essential

Even with correction:

- models hallucinate
- models generate bad inputs
- reasoning remains unreliable

Controllers continue enforcing workflow correctness.

---

# Final Understanding

Day 10 demonstrated that reliable AI workflows require:

- execution
- observations
- reflections
- corrections
- retries
- controller validation

The major realization was:

```text
A workflow should not stop after failure.

It should reflect, generate a correction, retry, and recover whenever possible.
```

---

# Technologies Used

- Python
- Ollama
- llama3.2:1b
- requests
- retrieval-aware workflows
- reflection systems
- correction systems
- retry systems
- controller-side validation
- ReAct workflows

---

# Example Final Output

```text
FINAL CONTROLLER ANSWER:

Today is Sunday, 31 May 2026.
15% of 5000 is 750.0.
The word Agentic has 7 characters.
```

---

# Repository

Main Repo:
https://github.com/gauradesh007/agentic-ai-30-days

Portfolio:
https://gauradesh007.github.io

LinkedIn:
https://www.linkedin.com/in/adesh-gaur/

---

# Most Important Day 10 Insight

```text
A reliable AI workflow should not stop after failure.

It should reflect, generate a correction, retry, and recover whenever possible.
```