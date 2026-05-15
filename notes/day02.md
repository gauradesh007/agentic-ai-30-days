# Day 2 Notes — Multi-Tool Controller Agent

# Overview

Day 2 focused on transforming a simple single-tool AI agent into a multi-tool controller-based agent.

The biggest lesson from today was:

> A reliable AI agent is not just a language model.
> It is a controlled workflow built around an unreliable model.

The local LLM frequently:
- hallucinated outputs
- invented fake dates
- generated invalid JSON
- suggested invalid tools
- ignored instructions

To handle this, the controller layer became the real intelligence system.

---

# Goal of Day 2

The objective was to build an agent that could:

- use multiple tools
- decide which tool to use
- track completed actions
- validate tool usage
- recover from unreliable model behavior
- stop when required tasks were complete

Example task:

What day is it today and what is 18% of 4500?

This required:
1. current_date tool
2. calculator tool

---

# Core Agent Architecture

User Question
   ↓
LLM Suggests Action
   ↓
JSON Extraction
   ↓
Controller Validates Action
   ↓
Tool Executes
   ↓
Observation Stored
   ↓
Controller Decides Next Step
   ↓
Loop Continues Until Done
   ↓
Final Controller Summary

Important insight:

The model suggests.
The controller decides.
The tools execute.

---

# Tools Implemented

## 1. calculator

Purpose:
- perform mathematical calculations

Example:

calculator("0.18 * 4500")

Output:

810.0

The calculator also handled malformed model input like:

18% 4500

which was automatically converted into:

18/100 * 4500

---

## 2. current_date

Purpose:
- retrieve the actual current system date

Example output:

Friday, 15 May 2026

This tool was important because the model repeatedly hallucinated fake dates.

---

## 3. text_length

Purpose:
- count characters in text

Example:

text_length("Agentic")

Output:

7

---

# Tool Registry

The project introduced a tool registry:

TOOLS = {
    "calculator": calculator,
    "current_date": current_date,
    "text_length": text_length
}

Benefits:
- dynamic tool execution
- scalable architecture
- centralized tool management

---

# Tool Aliases

The model often hallucinated invalid tool names like:

calculation
math
date

To fix this, aliases were introduced.

This normalized incorrect model outputs into valid tool names.

---

# Why JSON Extraction Was Necessary

The local model frequently returned outputs with extra text mixed with JSON.

This is not valid structured output.

To handle this, the project implemented:

extract_json_objects()

This function:
- scanned raw text
- extracted valid JSON blocks
- ignored broken text
- prevented parser crashes

Important lesson:

Never trust raw model output directly.
Always validate and extract structure.

---

# The Controller Layer

The controller became the most important part of the system.

Responsibilities:
- validate tool usage
- track completed tools
- prevent repeated actions
- select missing required tools
- normalize invalid tool names
- stop infinite loops

This was implemented using:

choose_next_action()

This function acted as a workflow manager.

---

# Required Tool Tracking

The project introduced:

required_tools = ["current_date", "calculator"]

This allowed the controller to know:
- which tasks were still incomplete
- which tools were still required

Without this, the model frequently wandered into unrelated actions like text_length.

---

# Observation and State

Tool results were stored in:

tool_results = {}

Example:

tool_results = {
    "current_date": "Friday, 15 May 2026",
    "calculator": "810.0"
}

This created memory/state inside the agent loop.

The observation step looked like:

Tool used: calculator
Tool result: 810.0

These observations were sent back to the model to continue reasoning.

This implemented the ReAct pattern:

Thought → Action → Observation → Next Action

---

# Stopping Conditions

A critical improvement was:

if all(tool in tool_results for tool in required_tools):
    break

This prevented:
- infinite loops
- repeated tool calls
- unnecessary reasoning

Reliable agents require explicit stopping conditions.

---

# Most Important Lessons From Day 2

## 1. Models are unreliable planners

The model:
- hallucinated dates
- invented tools
- produced malformed JSON
- ignored formatting instructions

This is normal behavior for small local models.

---

## 2. Prompting alone is not enough

Even strong prompts did not guarantee correct behavior.

Reliability came from:
- validation
- controller logic
- state tracking
- workflow constraints

---

## 3. The controller is the real intelligence layer

The controller:
- enforced rules
- validated actions
- tracked state
- controlled execution

Without the controller, the agent would fail repeatedly.

---

## 4. AI agents are workflow systems

Important realization:

Agent engineering is mostly workflow engineering.

The difficult part is not generating text.
The difficult part is:
- orchestration
- validation
- retries
- memory
- control flow
- state management

---

# Final Understanding

At the end of Day 2, the agent could:

- use multiple tools
- route tasks correctly
- recover from hallucinated outputs
- track workflow progress
- stop when complete
- generate a reliable final summary

Example final output:

Today is Friday, 15 May 2026.
18% of 4500 is 810.0.

---

# Most Important Insight

A reliable AI agent is a controlled workflow built around an unreliable model.

---

# Technologies Used

- Python
- Ollama
- llama3.2:1b
- requests
- JSON parsing
- local tool execution

---

# Repository

Main Repo:
https://github.com/gauradesh007/agentic-ai-30-days

Portfolio Website:
https://gauradesh007.github.io
