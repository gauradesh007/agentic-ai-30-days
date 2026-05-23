# Day 6 Notes — Dynamic Planning Agent

# Overview

Day 6 focused on building a planning-based AI workflow agent capable of:

- explicit task planning
- task decomposition
- planner-executor workflows
- task execution tracking
- controller-side action validation
- workflow progression management
- controller-driven action correction

The goal was to move beyond reactive workflows and begin building agents that explicitly plan and execute ordered tasks.

---

# Core Lesson

A reliable workflow agent requires more than reasoning and memory.

It also requires:

explicit planning

The Day 6 workflow introduced:
- task planning
- task sequencing
- task execution validation
- planner-executor separation

This created a much more structured workflow architecture.

---

# Day 6 Workflow Architecture

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

This introduced the first planner-executor workflow architecture in the learning journey.

---

# Planner vs Executor

Day 6 introduced an important architectural separation.

## Planner

Responsible for:
- creating tasks
- ordering tasks
- deciding workflow progression

The planner defines:

what should happen

---

## Executor

Responsible for:
- executing tools
- generating observations
- updating workflow state

The executor performs:

the actual action

---

## Controller

Responsible for:
- validating execution
- correcting wrong actions
- enforcing workflow reliability

The controller verifies:

execution matches the plan

---

# Tools Used

## current_date

Purpose:
- retrieve actual system date

Used because local models frequently hallucinated dates.

Example output:

Friday, 22 May 2026

---

## calculator

Purpose:
- execute mathematical calculations

Example:

calculator("0.18 * 2500")

Output:

450.0

---

# Planning State

The Day 6 workflow introduced multiple planning-specific states.

## task_plan

Stores the planned workflow tasks.

Example:

task_plan = [
    "Get current date",
    "Calculate 18% of 2500",
    "Generate final response"
]

Purpose:
- explicitly represent workflow structure
- define execution order
- guide reasoning and execution

This became the most important Day 6 architectural addition.

---

## completed_tasks

Tracks completed workflow steps.

Example:

completed_tasks = [
    "Get current date",
    "Calculate 18% of 2500"
]

Purpose:
- prevent repeated execution
- track workflow progression
- monitor incomplete tasks

---

## tool_results

Stores successful tool outputs.

Example:

tool_results = {
    "current_date": "Friday, 22 May 2026",
    "calculator": "450.0"
}

Purpose:
- preserve observations
- support final summary generation
- validate workflow completion

---

## thought_history

Stores model reasoning traces.

Example:

thought_history = [
    "It is today's day, which we don't know yet.",
    "The current task requires calculation, so the controller is correcting the action."
]

Purpose:
- inspect reasoning progression
- debug planning behavior
- analyze controller corrections

---

# Initial Planning

The workflow introduced:

create_initial_plan()

which generated:

[
    "Get current date",
    "Calculate 18% of 2500",
    "Generate final response"
]

This introduced explicit task decomposition into the workflow.

---

# Task Progression

The workflow introduced:

get_next_task(task_plan, completed_tasks)

This allowed the workflow to:
- retrieve the next incomplete task
- execute tasks sequentially
- track workflow progression

This created:

planned execution

instead of:

pure reactive execution

---

# Action Validation

One of the most important Day 6 improvements was:

expected_action_for_task()

This allowed the controller to validate:

Does the model action match the current planned task?

Example:

Task:

Calculate 18% of 2500

Expected action:

calculator

Model incorrectly generated:

current_date

The controller detected:

ACTION MISMATCH
Expected: calculator
Got: current_date

This introduced:

plan-aware action validation

---

# Controller Corrections

The controller introduced:

correct_action_for_task()

This allowed the controller to:
- override incorrect model actions
- force expected workflow behavior
- preserve plan integrity

Example correction:

{
    "thought": "The current task requires calculation, so the controller is correcting the action.",
    "action": "calculator",
    "input": "0.18 * 2500"
}

This was a major Day 6 reliability improvement.

---

# Example Workflow

## Step 1

Task:

Get current date

Model action:

current_date

Observation:

Friday, 22 May 2026

---

## Step 2

Task:

Calculate 18% of 2500

Model incorrectly generated:

current_date

Controller corrected:

calculator

Input:

0.18 * 2500

Observation:

450.0

---

## Step 3

Task:

Generate final response

Workflow completed successfully.

---

# Key Concepts Learned

- planner-executor architecture
- explicit task planning
- task decomposition
- task progression tracking
- action validation
- controller-side correction
- workflow orchestration
- plan-aware execution

---

# Most Important Insights

## 1. Planning improves workflow structure

Without planning:
- workflows are reactive
- execution becomes chaotic
- reasoning becomes inconsistent

Planning introduces:
- structure
- sequencing
- workflow control

---

## 2. Controllers must validate execution against plans

Even with planning:
- the model chose incorrect actions
- reasoning remained unreliable
- workflows still required enforcement

The controller ensured:

execution matches the plan

---

## 3. Planner and executor should be separated

This became one of the most important Day 6 architectural realizations.

Planning and execution are different responsibilities.

This separation is foundational for:
- autonomous agents
- orchestration systems
- multi-agent workflows

---

# Final Understanding

Day 6 demonstrated that reliable AI workflows require:

- planning
- execution tracking
- controller validation
- workflow progression
- plan-aware execution

The major realization was:

A planner defines what should happen.
An executor performs actions.
A controller verifies execution matches the plan.

---

# Technologies Used

- Python
- Ollama
- llama3.2:1b
- requests
- planner-executor workflows
- ReAct architecture
- controller-side validation
- workflow orchestration

---

# Example Final Output

FINAL CONTROLLER ANSWER:

Today is Friday, 22 May 2026.
18% of 2500 is 450.0.

---

# Repository

Main Repo:
https://github.com/gauradesh007/agentic-ai-30-days

Portfolio:
https://gauradesh007.github.io

LinkedIn:
https://www.linkedin.com/in/adesh-gaur/
