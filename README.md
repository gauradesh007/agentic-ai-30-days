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
- planning systems
- planner-executor workflows
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
| Day 6 | Dynamic Planning Agent | ✅ |

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

# Day 6 — Dynamic Planning Agent

Built a planning-based AI workflow agent capable of:
- explicit task planning
- task decomposition
- planner-executor workflows
- task execution tracking
- controller-side action validation
- workflow progression management
- controller-driven action correction

## New Architectural Capabilities
- task_plan workflow planning
- completed_tasks execution tracking
- planner-executor separation
- task-aware validation
- controller-side workflow correction
- plan-aware execution

## Planner-Executor Workflow

User Goal
      ↓
Planner
      ↓
Task Plan
      ↓
Executor
      ↓
Observation
      ↓
Plan Update
      ↓
Final Summary

## Important Concepts Learned
- planner-executor architecture
- explicit task planning
- task decomposition
- task progression tracking
- action validation
- workflow orchestration
- plan-aware execution

## Important Insight

A planner defines what should happen.
An executor performs actions.
A controller verifies execution matches the plan.

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
- Planning systems
- Planner-executor workflows
- AI workflow reliability

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
│   ├── day05.md
│   └── day06.md
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
├── day06-planning-agent/
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
- planner-executor workflows
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
- explicit planning
- controller enforcement

---

# Future Direction

Upcoming areas of exploration:
- dynamic planning
- vector databases
- semantic memory retrieval
- long-term memory
- autonomous workflows
- LangGraph
- multi-agent orchestration
- production-grade AI systems