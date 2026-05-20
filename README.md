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
- memory-aware reasoning
- controller-enforced reliability

---

# Goal

By the end of 30 days, I aim to independently:

- design AI agents
- build multi-tool workflows
- implement memory and retrieval systems
- orchestrate autonomous workflows
- build reliable controller architectures
- deploy production-ready AI applications
- create real-world workflow intelligence systems

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
| Day 5 | Memory-Aware ReAct Agent | ✅ |

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

## Important Insight

A model is not the agent.

The controller and workflow orchestration are the actual intelligence system.

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

# Day 5 — Memory-Aware ReAct Agent

Built a memory-aware AI workflow agent capable of:
- storing workflow memory
- retrieving previous observations
- using memory during reasoning
- preventing repeated actions
- maintaining workflow continuity
- improving controller-guided execution

## New Architectural Capabilities
- memory_store workflow memory
- memory retrieval
- memory updates
- memory-conditioned reasoning
- controller-guided memory utilization
- observation persistence across steps

## Memory Workflow

User Question
      ↓
Memory Retrieval
      ↓
Thought
      ↓
Action
      ↓
Tool Execution
      ↓
Observation
      ↓
Memory Update
      ↓
Next Thought
      ↓
Final Answer

## Example Memory State

memory_store = [
    "Tool current_date returned: Wednesday, 20 May 2026",
    "Tool calculator returned: 2100.0"
]

## Example Controller Improvement

Previously:
- the model repeatedly called current_date
- memory existed
- workflow behavior did not change

After controller improvements:
- repeated completed tools were blocked
- missing required tools were forced
- memory influenced workflow behavior

## Important Concepts Learned
- memory-aware workflows
- memory retrieval
- memory-conditioned planning
- controller-guided reasoning
- workflow continuity
- observation persistence

## Important Insight

Memory becomes valuable only when it changes workflow behavior.

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
- Memory-aware workflows
- AI workflow reliability
- State management

---

# Repository Structure

agentic-ai-30-days/
│
├── setup/
│   ├── setup_checklist.md
│   └── environment setup files
│
├── notes/
│   ├── day01.md
│   ├── day02.md
│   ├── day03.md
│   ├── day04.md
│   └── day05.md
│
├── resources/
│
├── projects/
│
├── day01-first-agent/
├── day02-multi-tool-agent/
├── day03-stateful-agent/
├── day04-react-agent/
├── day05-memory-agent/
│
├── README.md
└── .gitignore

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
- memory-aware workflows
- controller-driven orchestration

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

# Most Important Realizations So Far

Reliable AI systems are not built around perfect models.

Reliable AI systems are built around:
- controlled workflows
- validation
- observations
- retries
- state management
- reasoning inspection
- memory-aware execution
- controller enforcement

---

# Future Direction

Upcoming areas of exploration:
- dynamic planning agents
- vector databases
- semantic memory retrieval
- long-term memory
- autonomous workflows
- LangGraph
- multi-agent orchestration
- production-grade AI systems