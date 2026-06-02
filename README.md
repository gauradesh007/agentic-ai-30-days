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
- multi-agent systems
- local LLM systems

---

# Goal

By the end of 30 days, I aim to independently:

- design AI agents
- build multi-tool workflows
- implement memory and retrieval systems
- orchestrate autonomous workflows
- build reliable controller architectures
- coordinate multiple agents
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
|------|--------|---------|
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
| Day 11 | Multi-Agent Foundation | ✅ |

---

# Architecture Evolution

The journey so far has progressively introduced new architectural capabilities.

```text
Day 1
Tool Execution

Day 2
Controller

Day 3
Retries

Day 4
ReAct

Day 5
Memory

Day 6
Planning

Day 7
Tool Registry

Day 8
Retrieval

Day 9
Reflection

Day 10
Self-Correction

Day 11
Multi-Agent Coordination
```

This progression is intentionally designed so that every new capability builds on the previous one.

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

## Important Insight

A reliable AI agent is a controlled workflow built around an unreliable model.

---

# Day 3 — Stateful Retry Agent

Built a workflow agent capable of:

- retry handling
- failure tracking
- workflow memory
- retry limits
- observation persistence

## Important Insight

Reliable agents must be tested against failure paths, not just success paths.

---

# Day 4 — ReAct Workflow Agent

Built a ReAct-style workflow agent capable of:

- Thought → Action → Observation loops
- reasoning traces
- semantic validation
- observation-aware reasoning

## Important Insight

Reasoning traces improve explainability, but reasoning itself still requires validation.

---

# Day 5 — Memory-Aware ReAct Agent

Built a memory-aware workflow agent capable of:

- storing workflow memory
- retrieving observations
- memory-conditioned reasoning
- maintaining workflow continuity

## Important Insight

Memory becomes valuable only when it changes workflow behavior.

---

# Day 6 — Dynamic Planning Agent

Built a planning-based workflow agent capable of:

- task decomposition
- planner-executor architecture
- task execution tracking
- controller-side corrections

## Important Insight

A planner defines what should happen.

An executor performs actions.

A controller verifies execution matches the plan.

---

# Day 7 — Tool Registry Agent

Built a tool-aware workflow agent capable of:

- centralized tool management
- dynamic tool selection
- scalable orchestration
- controller-side validation

## Important Insight

A scalable AI workflow system requires:

- centralized tool management
- dynamic tool selection
- controller-side validation

---

# Day 8 — Retrieval-Aware Agent

Built a retrieval-aware workflow agent capable of:

- structured memory
- memory retrieval
- retrieval-aware reasoning
- primitive RAG-style behavior

## Important Insight

Retrieval improves reasoning context, but controllers still enforce workflow reliability.

---

# Day 9 — Self-Reflecting Agent

Built a self-reflecting workflow agent capable of:

- evaluating tool outcomes
- reflection history
- workflow self-evaluation
- execution inspection

## Important Insight

A workflow should not only execute actions.

It should also evaluate the quality of those actions through reflection.

---

# Day 10 — Self-Correcting Agent

Built a self-correcting workflow agent capable of:

- detecting failures
- generating corrections
- retrying failed actions
- primitive self-healing

## Important Insight

A workflow should not stop after failure.

It should reflect, generate a correction, retry, and recover whenever possible.

---

# Day 11 — Multi-Agent Foundation

Built the first multi-agent workflow system capable of:

- specialist agents
- controller routing
- agent registries
- workflow aggregation
- agent communication
- inter-agent messaging
- coordinator agents

## Multi-Agent Architecture

```text
Task
      ↓
Controller
      ↓
Agent Routing
      ↓
Specialist Agents
      ↓
Shared Results
      ↓
Coordinator Agents
      ↓
Agent Communication
      ↓
Final Output
```

## Specialist Agents

The workflow introduced:

```text
date_agent
math_agent
text_agent
summary_agent
report_agent
```

Each agent owns a single responsibility.

---

## Agent Registry

Day 11 introduced:

```python
AGENT_REGISTRY = {
    "date_agent": date_agent,
    "math_agent": math_agent,
    "text_agent": text_agent,
    "summary_agent": summary_agent,
    "report_agent": report_agent,
}
```

This created centralized agent management.

---

## Agent Router

The workflow introduced:

```python
choose_agent()
```

which became responsible for:

```text
Task
↓
Correct Agent
```

This is the first true agent-routing architecture in the learning journey.

---

## Workflow Aggregation

The first coordinator agent:

```text
summary_agent
```

used outputs generated by:

```text
date_agent
math_agent
text_agent
```

to create a combined summary.

This introduced:

```text
shared-result aggregation
```

---

## Agent Communication

Day 11 Part 3 introduced:

```python
send_message()
```

Example:

```python
send_message(
    "report_agent",
    "math_agent",
    "Please provide the calculation result."
)
```

Output:

```text
report_agent asks math_agent:
Please provide the calculation result.
```

The workflow introduced:

```text
report_agent
↓ asks
math_agent

report_agent
↓ asks
text_agent
```

This became the first:

```text
inter-agent communication
```

pattern in the learning journey.

---

## Important Concepts Learned

- multi-agent systems
- specialist agents
- agent routing
- workflow aggregation
- inter-agent messaging
- coordinator agents
- report generation

## Important Insight

Multi-Agent does not mean Multi-LLM.

Agents are responsibilities coordinated by a controller and connected through communication.

---

# Current Learning Direction

Current areas of focus:

- Agentic AI
- Workflow orchestration
- Multi-Agent Systems
- Local LLM Systems
- AI Controller Architectures
- ReAct Workflows
- Retrieval Systems
- Reflection Systems
- Self-Correcting Workflows
- Multi-Agent Coordination
- Agent Communication
- Agent Collaboration

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
│   ├── day10.md
│   └── day11.md
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
├── day11-multi-agent-foundation/
│
├── README.md
└── .gitignore
```

---

# Technologies Used

- Python
- Ollama
- GitHub
- Linux Mint
- VS Code
- ReAct Architecture
- Planner-Executor Workflows
- Tool Registries
- Retrieval Systems
- Reflection Systems
- Self-Correcting Workflows
- Multi-Agent Architectures

---

# Portfolio & Links

🌐 Portfolio

https://gauradesh007.github.io

💼 LinkedIn

https://www.linkedin.com/in/adesh-gaur/

📂 GitHub

https://github.com/gauradesh007

---

# Long-Term Goal

The long-term objective of this journey is to evolve from:

```text
Enterprise Integration Engineering
```

to:

```text
AI Workflow & Agent Systems Engineering
```

while building publicly documented proof-of-work throughout the process.

---

# Most Important Realizations So Far

Reliable AI systems are not built around perfect models.

Reliable AI systems are built around:

- controllers
- validation
- observations
- retries
- memory
- planning
- retrieval
- reflection
- correction
- coordination
- multi-agent coordination
- agent communication

Every day in this journey has reinforced that principle.

---

# Future Direction

Upcoming areas of exploration:

- Agent Communication
- Agent Delegation
- Multi-Agent Collaboration
- Long-Term Memory
- Vector Databases
- Semantic Retrieval
- Advanced RAG
- Autonomous Workflows
- LangGraph
- Production-Grade Agent Systems

---

# Most Important Insight So Far

```text
AI Engineering is not about making one model smarter.

It is about designing reliable systems around imperfect models.
```