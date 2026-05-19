# Agentic AI 30-Day Journey

This repository documents my hands-on 30-day journey to learn, build, and deploy Agentic AI systems from scratch.

The focus of this journey is not just using AI frameworks, but understanding how AI agents actually work internally through:
- tool execution
- workflow orchestration
- controller logic
- memory and state
- retries and failure handling
- local LLM workflows

---

# Goal

By the end of 30 days, I aim to independently:

- design AI agents
- build multi-tool workflows
- implement memory and retrieval systems
- orchestrate autonomous workflows
- deploy production-ready AI applications
- build reliable AI controller architectures

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

---

# Day 1 — First Tool-Using Agent

Built a local AI agent using:
- Ollama
- Python
- Tool execution loop
- JSON parsing
- Calculator tool

## Key Lessons
- LLMs are unreliable without validation
- JSON parsing often fails
- The controller loop is the real agent
- Tools improve reliability

---

# Day 2 — Multi-Tool Controller Agent

Built a controller-based AI agent capable of:
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
- Models are unreliable planners
- Controllers enforce reliability
- Tool orchestration requires workflow management
- Agent systems require stopping conditions
- State tracking is critical for multi-step tasks

## Example Capability

Question:
What day is it today and what is 18% of 4500?

Final Output:
Today is Friday, 15 May 2026. 18% of 4500 is 810.0.

## Important Insight

A reliable AI agent is a controlled workflow built around an unreliable model.

---

# Day 3 — Stateful Retry Agent

Built a stateful AI workflow agent capable of:
- retry handling
- failure tracking
- workflow state management
- observation memory
- stopping conditions
- incomplete-task reporting

## Features Added
- tool_results state tracking
- failure_history logging
- retry_count management
- retry limits
- failure-aware workflow execution

## Example State Tracking

Successful state:

tool_results = {
    "current_date": "Monday, 18 May 2026",
    "calculator": "1364.0"
}

Failure state:

failure_history = [
    {
        "tool": "calculator",
        "input": "twenty two percent of 6200",
        "error": "ERROR: Invalid expression"
    }
]

## Key Concepts Learned
- Agent state management
- Failure-path testing
- Retry logic
- Observation-aware workflows
- Workflow reliability engineering

## Important Insight

Reliable agents are not built around perfect models.

Reliable agents are built around:
- controlled workflows
- validation
- retries
- state tracking
- failure handling

---

# Current Learning Direction

Current areas of focus:
- Agentic AI
- Workflow orchestration
- Multi-tool AI agents
- Local LLM systems
- AI controller architectures
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
