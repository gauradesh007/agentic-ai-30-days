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
- tool registries
- retrieval-aware workflows
- reflection systems
- self-correcting workflows
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
- Workflow-Based AI Controllers

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
| Day 7 | Tool Registry Agent | ✅ |
| Day 8 | Retrieval-Aware Agent | ✅ |
| Day 9 | Self-Reflecting Agent | ✅ |
| Day 10 | Self-Correcting Agent | ✅ |

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

# Day 7 — Tool Registry Agent

Built a tool-aware AI workflow agent capable of:

- centralized tool management
- dynamic tool selection
- tool metadata reasoning
- controller-side validation
- fallback execution
- scalable orchestration

## New Architectural Capabilities

- TOOL_REGISTRY architecture
- tool metadata
- tool descriptions
- dynamic tool selection
- controller fallback execution
- scalable workflow orchestration

## Important Concepts Learned

- tool registries
- dynamic tool selection
- workflow scalability
- controller-side validation
- fallback execution
- tool-aware orchestration

## Important Insight

A scalable AI workflow system requires:

- centralized tool management
- dynamic tool selection
- controller-side validation
- tool-aware orchestration

---

# Day 8 — Retrieval-Aware Agent

Built a retrieval-aware AI workflow agent capable of:

- structured memory storage
- relevant memory retrieval
- retrieval-aware reasoning
- retrieval-enhanced fallback logic
- context-aware workflow execution
- retrieval-conditioned controller decisions

## New Architectural Capabilities

- MEMORY_DB structured memory
- retrieval-aware reasoning
- keyword-based memory retrieval
- retrieval-conditioned execution
- retrieval-enhanced fallback logic
- retrieval-aware orchestration

## Retrieval Workflow

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
Final Summary
```

## Important Concepts Learned

- retrieval-aware workflows
- structured memory databases
- retrieval-augmented reasoning
- retrieval-conditioned execution
- primitive RAG architectures
- retrieval-aware orchestration

## Important Insight

Retrieval improves reasoning context, but controllers still enforce workflow reliability.

---

# Day 9 — Self-Reflecting Agent

Built a self-reflecting AI workflow agent capable of:

- evaluating its own actions
- inspecting tool results
- generating workflow reflections
- maintaining reflection history
- performing primitive self-critique
- improving workflow observability
- introducing workflow self-evaluation

## New Architectural Capabilities

- reflection_history
- reflection-aware execution
- workflow self-evaluation
- observation inspection
- reflection logging
- reflection-driven observability

## Reflection Workflow

```text
User Question
      ↓
Memory Retrieval
      ↓
Relevant Context
      ↓
Tool Selection
      ↓
Tool Execution
      ↓
Observation
      ↓
Reflection
      ↓
Reflection History
      ↓
Final Summary
```

## Important Concepts Learned

- self-reflecting workflows
- workflow evaluation
- reflection history
- observation inspection
- execution analysis
- primitive self-critique
- reflection-aware orchestration

## Important Insight

A reliable AI workflow should not only execute actions.

It should also evaluate the quality of those actions through reflection.

---

# Day 10 — Self-Correcting Agent

Built a self-correcting AI workflow agent capable of:

- detecting failed tool executions
- generating correction recommendations
- retrying failed actions automatically
- maintaining correction history
- maintaining retry history
- combining reflection and correction
- performing primitive self-healing

## New Architectural Capabilities

- correction_history
- retry_history
- correction generation
- automated retries
- self-healing workflows
- reflection-driven recovery

## Self-Correcting Workflow

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

## Important Concepts Learned

- self-correcting workflows
- correction systems
- retry mechanisms
- self-healing execution
- reflection-driven recovery
- controller-guided correction
- primitive autonomous recovery

## Important Insight

A workflow should not stop after failure.

It should reflect, generate a correction, retry, and recover whenever possible.

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
- Tool registries
- Retrieval-aware workflows
- Reflection systems
- Self-correcting workflows
- AI workflow reliability

---

# Repository Structure

```text
agentic-ai-30-days/
│
├── setup/
│   └── setup_checklist.md
│
├── notes/
│   ├── day01.md
│   ├── day02.md
│   ├── day03.md
│   ├── day04.md
│   ├── day05.md
│   ├── day06.md
│   ├── day07.md
│   ├── day08.md
│   ├── day09.md
│   └── day10.md
│
├── resources/
├── projects/
│
├── day01-first-agent/
├── day02-multi-tool-agent/
├── day03-stateful-agent/
├── day04-react-agent/
├── day05-memory-agent/
├── day06-planning-agent/
├── day07-tool-registry-agent/
├── day08-retrieval-agent/
├── day09-reflection-agent/
├── day10-self-correcting-agent/
│
├── README.md
└── .gitignore
```

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
- tool registries
- retrieval-aware workflows
- reflection systems
- self-correcting systems
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
- centralized tool management
- retrieval-aware orchestration
- reflection-aware evaluation
- self-correcting behavior
- controller enforcement

---

# Future Direction

Upcoming areas of exploration:

- multi-agent systems
- agent communication
- task delegation
- vector databases
- semantic retrieval
- long-term memory
- autonomous workflows
- LangGraph
- production-grade AI systems
- advanced RAG architectures
- self-improving agent systems