# Day 1 — First Tool-Using Agent

## Goal

Build a local AI agent using Ollama that can:
- reason about a task
- decide to use a calculator tool
- execute the tool
- return a final answer

## Stack

- Python
- Ollama
- llama3.2:1b
- requests

## Features

- Local LLM
- Tool calling
- JSON parsing
- Error recovery
- Calculator execution

## Lessons Learned

- LLMs are unreliable without validation
- JSON parsing often fails
- The control loop is the actual agent
- Tools improve reliability

## Example

Question:
What is 18% of 2500?

Answer:
450