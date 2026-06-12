# Day 22 — AutoGen Foundations

## Objective

Day 22 focused on learning Microsoft's AutoGen framework and understanding how conversation-driven multi-agent systems differ from task-driven frameworks such as CrewAI.

The goal was to understand:

- AutoGen agents
- agent conversations
- multi-agent communication
- conversation orchestration
- role-constrained conversations
- termination control
- agent collaboration through dialogue

Day 22 introduced the first:

```text
Conversation-Centric Multi-Agent Framework
```

in the learning journey.

---

# Core Lesson

Day 21 introduced:

```text
CrewAI
↓
Agent
↓
Task
↓
Crew
↓
Result
```

Day 22 introduced:

```text
Agent
↔
Agent
↔
Agent
↓
Conversation
↓
Result
```

This became the first:

```text
Conversation-Driven Agent Workflow
```

---

# Why AutoGen Matters

CrewAI is:

```text
Task-Centric
```

You define:

```text
Task
↓
Agent
↓
Execution
```

AutoGen is:

```text
Conversation-Centric
```

You define:

```text
Agent
↓
Conversation
↓
Decision
```

This difference became the most important lesson of Day 22.

---

# Day 22 Architecture

```text
User
      ↓
Agent
      ↕
Agent
      ↕
Agent
      ↓
Conversation
      ↓
Result
```

This architecture enables collaborative reasoning through dialogue.

---

# Local LLM Integration

Day 22 used:

```text
Ollama
+
llama3.2:1b
```

through:

```python
OpenAIChatCompletionClient()
```

configured against:

```text
http://localhost:11434/v1
```

This allowed AutoGen to run entirely on local infrastructure.

---

# Part 1 — First AutoGen Conversation

Day 22 Part 1 introduced:

```python
AssistantAgent()
```

and:

```python
run_stream()
```

Example:

```python
assistant = AssistantAgent(...)
```

The first workflow became:

```text
User
↓
Assistant Agent
↓
Response
```

---

# Part 1 Architecture

```text
User Message
      ↓
Assistant Agent
      ↓
Generated Response
```

This became the first AutoGen workflow.

---

# AssistantAgent

Day 22 introduced:

```python
AssistantAgent
```

Purpose:

```text
Respond to messages
Participate in conversations
Generate reasoning
```

This is the foundational AutoGen agent type.

---

# Streaming Responses

Day 22 introduced:

```python
run_stream()
```

and:

```python
Console(stream)
```

Workflow:

```text
Conversation
↓
Message Stream
↓
Console Output
```

This differs from CrewAI's:

```python
kickoff()
```

execution model.

---

# Part 2 — Multi-Agent Conversation

Day 22 Part 2 introduced:

```text
research_agent
↓
writer_agent
```

inside:

```python
RoundRobinGroupChat
```

This created the first:

```text
Multi-Agent AutoGen Conversation
```

---

# RoundRobinGroupChat

Purpose:

```text
Agent A
↓
Agent B
↓
Agent A
↓
Agent B
```

until termination occurs.

This became the first:

```text
Conversation-Orchestrated Team
```

workflow.

---

# Multi-Agent Architecture

```text
User
      ↓
Research Agent
      ↓
Writer Agent
      ↓
Research Agent
      ↓
Writer Agent
```

Unlike CrewAI, agents communicate through dialogue.

---

# Part 3 — Reviewer Agent

Day 22 Part 3 introduced:

```text
Research Agent
↓
Writer Agent
↓
Reviewer Agent
```

The reviewer became responsible for:

- reviewing explanations
- checking clarity
- checking accuracy
- suggesting improvements

This became the first:

```text
AutoGen Review Workflow
```

---

# Termination Control

Day 22 introduced:

```python
MaxMessageTermination()
```

Example:

```python
termination = MaxMessageTermination(
    max_messages=4
)
```

Purpose:

```text
Prevent Infinite Conversations
```

This became the first:

```text
Conversation Control Layer
```

---

# Part 4 — Role-Constrained Conversations

Day 22 Part 4 introduced:

```text
Research Agent
↓
Research Only

Writer Agent
↓
Writing Only

Reviewer Agent
↓
Review Only
```

through stronger:

```python
system_message
```

definitions.

This became the first:

```text
Role-Constrained AutoGen Workflow
```

---

# Important Discovery — Role Drift

Even with role constraints, AutoGen agents still exhibited:

```text
Role Drift
```

Example:

```text
Research Agent
↓
Research
Writing
Reviewing
```

instead of:

```text
Research Agent
↓
Research Only
```

---

# What Is Role Drift?

Role drift occurs when:

```text
Agent A
↓
Performs Agent B's Responsibilities
```

This became one of the most important Day 22 lessons.

---

# Why Role Drift Happens

AutoGen agents are fundamentally:

```text
Conversation Participants
```

rather than:

```text
Strict Task Executors
```

The model often attempts to be helpful and complete the entire task.

This causes:

```text
Role Expansion
```

beyond the assigned responsibility.

---

# CrewAI vs AutoGen

## CrewAI

```text
Task-Centric
Structured
Predictable
```

Architecture:

```text
Task
↓
Agent
↓
Result
```

---

## AutoGen

```text
Conversation-Centric
Flexible
Less Predictable
```

Architecture:

```text
Agent
↔
Agent
↔
Agent
↓
Conversation
↓
Result
```

---

# Most Important Day 22 Realization

Day 22 demonstrated:

```text
Framework
≠
Behavior Control
```

Even with:

```text
Roles
Prompts
Instructions
```

LLMs may still:

```text
Interpret
```

rather than:

```text
Strictly Execute
```

instructions.

---

# Example Workflow

## Step 1

Create agents.

Result:

```text
Research Agent
Writer Agent
Reviewer Agent
```

---

## Step 2

Create team.

Result:

```text
RoundRobinGroupChat
```

---

## Step 3

Configure termination.

Result:

```text
MaxMessageTermination
```

---

## Step 4

Start conversation.

Result:

```text
Agent Discussion
```

---

## Step 5

Observe collaboration.

Result:

```text
Research
↓
Writing
↓
Review
```

---

## Step 6

Observe role drift.

Result:

```text
Agents performing extra work
```

---

# Day 22 Workflow Evolution

Part 1:

```text
Single Agent Conversation
```

Part 2:

```text
Multi-Agent Conversation
```

Part 3:

```text
Reviewer Agent
```

Part 4:

```text
Role-Constrained Conversations
```

---

# Key Concepts Learned

- AutoGen
- AssistantAgent
- AgentChat
- RoundRobinGroupChat
- Conversation Workflows
- Reviewer Agents
- Termination Conditions
- Role Constraints
- Role Drift

---

# Most Important Insights

## 1. AutoGen Is Conversation-Centric

Agents collaborate through conversation rather than task execution.

---

## 2. Conversations Require Control

Without termination conditions:

```text
Agents Can Continue Indefinitely
```

---

## 3. Role Constraints Are Important

Clear roles improve conversation quality.

---

## 4. Role Drift Is Real

Agents often perform responsibilities outside their assigned role.

---

## 5. AutoGen Prioritizes Flexibility

Compared to CrewAI:

```text
More Flexible
Less Predictable
```

---

# Technologies Used

- Python
- AutoGen
- AgentChat
- Ollama
- llama3.2:1b
- Multi-Agent Conversations
- Termination Control

---

# Relationship To Previous Days

Day 22 built directly on:

```text
Day 11
Multi-Agent Foundation

Day 13
Collaboration

Day 14
Coordination

Day 15
Teams

Day 21
CrewAI
```

while introducing a completely different orchestration philosophy.

---

# Future Improvements

Possible next improvements:

- Group Chat Managers
- Human-in-the-Loop Workflows
- AutoGen Tools
- AutoGen Memory
- LangGraph
- Production Multi-Agent Systems

---

# Most Important Day 22 Insight

```text
CrewAI organizes work through tasks.

AutoGen organizes work through conversations.

Understanding both approaches is essential for building production multi-agent systems.
```