# Agentic AI 30-Day Journey

This repository documents my hands-on 30-day journey to learn, build, and deploy Agentic AI systems from scratch.

The focus of this journey is not just using AI frameworks, but understanding how AI agents actually work internally through:
- tool execution
- workflow orchestration
- controller logic
- memory and state
- retries and failure handling
- reasoning-aware workflows
- ReAct architecture
- local LLM systems

---

# Goal

By the end of 30 days, I aim to independently:

- design AI agents
- build multi-tool workflows
- implement memory and retrieval systems
- orchestrate autonomous workflows
- build reliable controller architectures
- deploy production-ready AI applications

---

# Current Stack

- Python
- Linux Mint
- VS Code
- GitHub
- Ollama
- Local LLMs
- Workflow-based AI Controllers

---

# Progress

| Day | Topic | Status |
|---|---|---|
| Day 1 | Setup + First Tool-Using Agent | ✅ |
| Day 2 | Multi-Tool Controller Agent | ✅ |
| Day 3 | Stateful Retry Agent | ✅ |
| Day 4 | ReAct Workflow Agent | ✅ |

---

# Day 1 — First Tool-Using Agent

Built a local AI agent using:
- Ollama
- Python
- tool execution loop
- JSON parsing
- calculator tool

## Key Lessons
- LLMs are unreliable without validation
- JSON parsing frequently fails
- the controller loop is the real agent
- tools improve reliability

---

# Day 2 — Multi-Tool Controller Agent

Built a controller-based AI workflow agent capable of:
- multi-tool orchestration
- tool routing
- JSON extraction
- workflow validation
- observation tracking
- state management

## Tools Used
- calculator
- current_date
- text_length

## Key Concepts Learned
- models are unreliable planners
- controllers enforce reliability
- workflow orchestration requires state
- stopping conditions are essential
- AI workflows require validation

## Example Capability

Question:

What day is it today and what is 18% of 4500?

Final Output:

Today is Friday, 15 May 2026.
18% of 4500 is 810.0.

## Important Insight

A reliable AI agent is a controlled workflow built around an unreliable model.

---

# Day 3 — Stateful Retry Agent

Built a stateful workflow agent capable of:
- retry handling
- failure tracking
- workflow memory
- observation persistence
- retry limits
- incomplete-task reporting

## Features Added
- tool_results state tracking
- failure_history logging
- retry_count management
- failure-aware execution
- stopping conditions

## Example Failure Tracking

failure_history = [
    {
        "tool": "calculator",
        "input": "twenty two percent of 6200",
        "error": "ERROR: Invalid expression"
    }
]

## Key Concepts Learned
- workflow state
- retry logic
- failure-path testing
- observation memory
- defensive programming

## Important Insight

Happy-path demos are insufficient.

Reliable agents must be tested against failure paths.

---

# Day 4 — ReAct Workflow Agent

Built a ReAct-style workflow agent capable of:
- explicit reasoning traces
- Thought → Action → Observation loops
- semantic validation
- observation-aware reasoning
- reasoning inspection
- workflow explainability

## New Architectural Capabilities
- thought_history tracking
- semantic calculator validation
- reasoning-aware workflows
- observation-driven planning
- controller-side reasoning enforcement

## ReAct Workflow

Thought
↓
Action
↓
Observation
↓
Next Thought

## Example Reasoning Trace

{
  "thought": "To answer the question, I first need today's date.",
  "action": "current_date",
  "input": ""
}

Observation:

Tuesday, 19 May 2026

Next reasoning:

{
  "thought": "Now I need to calculate 15% of 9600.",
  "action": "calculator",
  "input": "0.15 * 9600"
}

Observation:

1440.0

## Important Concepts Learned
- ReAct architecture
- reasoning traces
- semantic validation
- observation-aware workflows
- reasoning hallucinations
- controller-side reasoning checks

## Important Insight

Reasoning traces improve explainability, but reasoning itself still requires validation.

---

# Current Learning Direction

Current areas of focus:
- Agentic AI
- Workflow orchestration
- Multi-tool AI agents
- Local LLM systems
- AI controller architectures
- ReAct workflows
- Semantic validation
- AI workflow reliability
- Memory and state management

---

# Technologies Used

- Python
- Ollama
- llama3.2:1b
- requests
- GitHub
- Linux Mint
- VS Code
- ReAct workflow architecture

---

# Portfolio & Links

🌐 Portfolio:
https://gauradesh007.github.io

💼 LinkedIn:
https://www.linkedin.com/in/adesh-gaur/

📂 GitHub:
https://github.com/gauradesh007

---

# Long-Term Goal

The long-term objective of this journey is to evolve from:
- enterprise integration engineering

to:
- AI workflow and agent systems engineering

while building publicly documented proof-of-work throughout the process.

---

# Most Important Realization So Far

Reliable AI systems are not built around perfect models.

Reliable AI systems are built around:
- controlled workflows
- validation
- observations
- retries
- state management
- reasoning inspection
- controller enforcement
