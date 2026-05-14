# Day 1 Notes — First Tool-Using Agent

## 1. What is an AI agent?

An AI agent is a system that can take a goal, reason about what actions are needed, use tools, observe results, and continue until it produces a final answer.

A normal chatbot only generates text responses. An agent can interact with tools, APIs, memory, files, or external systems.

The core agent loop is:

Goal → Reason → Act → Observe → Repeat → Final Answer

Today I built a simple version of this loop using Python and Ollama.


---

## 2. Why are tools necessary?

LLMs are not reliable at:
- math
- real-time information
- precise calculations
- external actions

For example, when I directly asked the local model a math question, it answered incorrectly.

Tools improve reliability because:
- the model decides WHAT to do
- the tool performs the actual computation or action

In my project:
- the model decided to use the calculator
- Python executed the math correctly


---

## 3. What failures did I encounter today?

I encountered multiple failures:
- OpenAI API quota error
- malformed JSON output from the model
- timeout errors from Ollama
- extra brackets in JSON
- multiple JSON responses instead of one

These failures showed me that AI systems are unreliable without validation and control logic.


---

## 4. Why did the JSON parsing fail?

The local model sometimes generated invalid JSON because small local models are less reliable at following strict formatting instructions.

Examples of failures:
- extra closing brackets
- two JSON objects instead of one
- nested JSON strings

JSON parsing failed because Python expects valid structured JSON.


---

## 5. What role does clean_json() play?

The clean_json() function acts as a defensive layer between the model and the application.

It:
- extracts the JSON object
- removes invalid extra brackets
- prevents crashes
- improves robustness

This taught me that real AI systems need validation and recovery logic.


---

## 6. What is the difference between the model and the agent?

The model is only the reasoning engine that generates text.

The agent is the complete system that includes:
- prompts
- tools
- control logic
- parsing
- retries
- memory
- validation

The model alone is not reliable enough to be considered an agent.


---

## 7. Why are local models less reliable?

Local models are usually:
- smaller
- less powerful
- running on CPU
- optimized for speed and low hardware usage

Because of this:
- reasoning quality is lower
- instruction following is weaker
- formatting consistency is worse

However, they are useful for learning because they expose problems clearly.


---

## 8. What I learned today

Today I learned:
- how to install and use Ollama
- how local LLMs work
- how agents use tools
- how JSON-based control loops work
- why validation is necessary
- why agent engineering is more than prompting

I also learned that debugging and handling failures is part of building AI systems.


---

## 9. Evidence

GitHub Repo:
https://github.com/gauradesh007/agentic-ai-30-days

Portfolio Website:
https://gauradesh007.github.io