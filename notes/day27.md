# Day 27 Notes — Tool Calling Agents

# Overview

Day 27 focused on introducing tool usage into agent workflows and understanding how production agents interact with external capabilities.

The goal was to understand:

- tool execution
- tool-aware agents
- tool selection
- LLM-driven tool routing
- tool validation
- guard rails
- workflow reliability

Day 27 introduced the first:

```text
Tool Calling Agent Workflow
```

in the learning journey.

---

# Core Lesson

Day 26 introduced:

```text
AI
↓
Review
↓
Human Approval
```

Day 27 introduced:

```text
Question
↓
Tool Selection
↓
Tool Execution
↓
Validation
↓
Answer
```

This became the first:

```text
Tool-Aware Agent Workflow
```

---

# Why Day 27 Matters

Until Day 26, agents could:

```text
Research
Write
Review
Approve
```

But they could not:

```text
Use External Tools
```

Day 27 changed that.

The workflow became:

```text
Think
↓
Select Tool
↓
Execute Tool
↓
Validate Result
↓
Respond
```

This is one of the core patterns used in production AI systems.

---

# Day 27 Workflow Architecture

```text
START
      ↓
Tool Selection Agent
      ↓
Tool Execution Agent
      ↓
Tool Review Agent
      ↓
END
```

This became the first:

```text
Tool Calling LangGraph Workflow
```

---

# Workflow State

Day 27 introduced:

```python
class WorkflowState(TypedDict):
    question: str
    tool: str
    answer: str
    review: str
```

Purpose:

```text
Track:
Question
Selected Tool
Tool Result
Validation Review
```

---

# Tools

Day 27 introduced:

```python
calculator_tool()
date_tool()
```

These became the first:

```text
Reusable Agent Tools
```

inside a LangGraph workflow.

---

# Calculator Tool

Purpose:

```text
Perform Calculations
```

Example:

```text
25% of 400
```

Result:

```text
100.0
```

---

# Date Tool

Purpose:

```text
Return Current Date
```

Example:

```text
What is today's date?
```

Result:

```text
2026-06-18
```

---

# Part 1 — First Tool Agent

Day 27 Part 1 introduced:

```text
Tool Agent
↓
Calculator Tool
↓
Answer
```

Architecture:

```text
START
↓
Tool Agent
↓
Calculator Tool
↓
END
```

This became the first:

```text
Tool Execution Workflow
```

---

# Hardcoded Tool Selection

Part 1 used:

```python
calculator_tool(
    25,
    400,
)
```

The tool was selected manually.

Purpose:

```text
Learn Tool Execution
```

before introducing dynamic selection.

---

# Part 2 — LLM Tool Selection

Day 27 Part 2 introduced:

```text
LLM
↓
Choose Tool
↓
Execute Tool
```

The workflow became:

```text
Question
↓
LLM
↓
Tool
↓
Answer
```

---

# Tool Selection Agent

Day 27 introduced:

```python
tool_selection_agent()
```

Responsibilities:

```text
Read Question
Choose Tool
Store Tool Choice
```

This became the first:

```text
Tool Routing Agent
```

---

# Example

Question:

```text
What is 25% of 400?
```

Tool Selected:

```text
calculator
```

---

# Example

Question:

```text
What is today's date?
```

Expected Tool:

```text
date
```

---

# Major Discovery

The LLM selected:

```text
calculator
```

for:

```text
What is today's date?
```

This revealed an important lesson:

```text
LLM Tool Selection
≠
Reliable Tool Selection
```

---

# Production Lesson

Day 27 demonstrated:

```text
Free-Form LLM Decisions
↓
Workflow Risk
```

The wrong tool can be selected.

This created the need for validation.

---

# Part 3 — Guarded Tool Selection

Day 27 Part 3 introduced:

```python
normalize_tool_choice()
```

Purpose:

```text
Validate Tool Choice
Correct Tool Choice
```

This became the first:

```text
Tool Selection Guard
```

---

# Guard Architecture

Instead of:

```text
LLM
↓
Tool
```

the workflow became:

```text
LLM
↓
Guard
↓
Tool
```

This is a common production pattern.

---

# Example Guard Rule

```python
if "today" in question:
    return "date"
```

Purpose:

```text
Prevent Incorrect Tool Selection
```

---

# Corrected Workflow

Question:

```text
What is today's date?
```

LLM:

```text
calculator
```

Guard:

```text
date
```

Result:

```text
Correct Tool Executed
```

---

# Part 4 — Tool Result Review

Day 27 Part 4 introduced:

```python
tool_review_agent()
```

Purpose:

```text
Validate Tool Result
```

instead of blindly trusting execution.

---

# Initial Problem

The LLM reviewer incorrectly claimed:

```text
The correct tool was not selected.
```

even when:

```text
date
```

was clearly correct.

This revealed another lesson:

```text
LLM Validation
≠
Reliable Validation
```

---

# Rule-Based Validation

Day 27 introduced:

```python
validate_tool_result()
```

Purpose:

```text
Question
↓
Tool
↓
Validation
```

using deterministic logic.

---

# Validation Architecture

Instead of:

```text
Tool
↓
LLM Review
```

the workflow became:

```text
Tool
↓
Rule Validation
```

This increased reliability.

---

# Complete Workflow

```text
START
      ↓
Tool Selection Agent
      ↓
LLM Tool Suggestion
      ↓
Tool Guard
      ↓
Tool Execution Agent
      ↓
Tool Review Agent
      ↓
END
```

---

# Final Execution Flow

```text
Question
↓
Tool Selection
↓
Guard Validation
↓
Tool Execution
↓
Result Validation
↓
Final Answer
```

This became the first:

```text
Reliable Tool Calling Workflow
```

---

# Example Workflow

## Step 1

Question received.

Example:

```text
What is today's date?
```

---

## Step 2

Tool Selection Agent executes.

Result:

```text
date
```

---

## Step 3

Guard validates tool.

Result:

```text
Correct Tool
```

---

## Step 4

Tool Execution Agent executes.

Result:

```text
2026-06-18
```

---

## Step 5

Tool Review Agent validates.

Result:

```text
Tool selection is valid.
```

---

# Day 27 Workflow Evolution

Part 1:

```text
Hardcoded Tool Execution
```

Part 2:

```text
LLM Tool Selection
```

Part 3:

```text
Guarded Tool Selection
```

Part 4:

```text
Tool Result Review
```

---

# Key Concepts Learned

- Tool Calling Agents
- Tool Execution
- Tool Routing
- LLM Tool Selection
- Tool Guards
- Validation Layers
- Reliable Tool Usage
- Production Tool Patterns

---

# Most Important Insights

## 1. Agents Need Tools

Production agents do more than generate text.

---

## 2. LLM Tool Selection Is Imperfect

The wrong tool may be selected.

---

## 3. Guards Improve Reliability

Rule-based validation protects workflows.

---

## 4. Validation Is Essential

Tool execution should be verified.

---

## 5. Production Systems Use Layers

Reliable workflows often look like:

```text
LLM
↓
Guard
↓
Tool
↓
Validation
```

rather than:

```text
LLM
↓
Tool
```

---

# Final Understanding

Day 27 demonstrated that production-grade tool agents require:

- tool selection
- tool execution
- tool validation
- guard rails
- workflow reliability

The major realization was:

```text
LLMs can choose tools.

But reliable systems do not blindly trust LLM decisions.

Production agent systems use guards,
validation, and deterministic checks
to ensure tools are selected and executed correctly.
```

---

# Technologies Used

- Python
- LangGraph
- ChatOllama
- Ollama
- llama3.2:1b
- Tool Calling
- Tool Routing
- Validation Workflows

---

# Repository

Main Repo:
https://github.com/gauradesh007/agentic-ai-30-days

Portfolio:
https://gauradesh007.github.io

LinkedIn:
https://www.linkedin.com/in/adesh-gaur/

---

# Relationship To Previous Days

Day 27 built directly on:

```text
Day 1
Tool Agent

Day 24
LangGraph + LLM Workflows

Day 25
Multi-Agent LangGraph

Day 26
Human-in-the-Loop Workflows
```

while introducing production-style tool usage.

---

# Future Improvements

Possible next improvements:

- Multiple Tool Selection
- Tool Chains
- Retrieval Tools
- Memory Tools
- RAG Agents
- Enterprise Integration Tools
- EDI Validation Tools

---

# Most Important Day 27 Insight

```text
LLMs can choose tools.

But reliable systems do not blindly trust LLM decisions.

Production agent systems use guards,
validation, and deterministic checks
to ensure tools are selected and executed correctly.
```
