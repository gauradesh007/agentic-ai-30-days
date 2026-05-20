import json
import requests
from datetime import datetime

# Ollama local API endpoint and model name.
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"


# -------------------
# TOOLS
# -------------------

def calculator(expression: str) -> str:
    """
    Executes a simple math expression.

    Example:
    "0.25 * 8400" -> "2100.0"
    """

    try:
        expression = expression.strip()

        # Convert percentage syntax into Python-friendly math.
        # Example: "25%" becomes "25/100"
        expression = expression.replace("%", "/100")

        # Basic safety check before using eval.
        # This prevents letters or unsafe characters from being executed.
        allowed = "0123456789+-*/(). "

        if not all(char in allowed for char in expression):
            return "ERROR: Invalid expression"

        return str(eval(expression))

    except Exception as e:
        return f"ERROR: {e}"


def current_date() -> str:
    """
    Returns the real current system date.

    This prevents the model from hallucinating today's date.
    """

    return datetime.now().strftime("%A, %d %B %Y")


# Tool registry.
# The controller can call tools dynamically by name.
TOOLS = {
    "calculator": calculator,
    "current_date": current_date
}


# -------------------
# OLLAMA CALL
# -------------------

def call_ollama(messages):
    """
    Sends the conversation history to Ollama and returns the model response text.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=600
    )

    response.raise_for_status()

    return response.json()["message"]["content"]


# -------------------
# JSON EXTRACTION
# -------------------

def extract_json_objects(text: str):
    """
    Extracts valid JSON objects from messy model output.

    Local models often return extra text or multiple JSON blocks.
    This function scans the text and extracts usable JSON objects.
    """

    text = text.strip()

    objects = []
    stack = 0
    start = None

    for i, char in enumerate(text):

        if char == "{":
            if stack == 0:
                start = i
            stack += 1

        elif char == "}":
            stack -= 1

            if stack == 0 and start is not None:
                candidate = text[start:i + 1]

                try:
                    objects.append(json.loads(candidate))
                except:
                    # Ignore malformed JSON blocks.
                    pass

    return objects


# -------------------
# AGENT STATE
# -------------------

user_question = "What day is it today and what is 25% of 8400?"

# These tools must complete successfully before the agent can finish.
required_tools = ["current_date", "calculator"]

# Stores successful tool outputs.
tool_results = {}

# Stores model reasoning traces.
thought_history = []

# Stores useful observations across the workflow.
memory_store = []

MAX_STEPS = 6


# -------------------
# SYSTEM PROMPT
# -------------------

messages = [
    {
        "role": "system",
        "content": """
You are a memory-aware ReAct AI workflow agent.

You must:
- reason step-by-step
- use observations
- use memory
- think before acting

Always return EXACTLY ONE JSON object.

Format:

{
  "thought": "reasoning",
  "action": "tool_name",
  "input": "tool input"
}

OR

{
  "thought": "reasoning",
  "action": "final",
  "answer": "final response"
}

Available tools:
- current_date
- calculator

Rules:
- Never explain outside JSON
- Use one action at a time
- Use calculator for math
- Use current_date for today's date
- Think carefully before acting
"""
    },
    {
        "role": "user",
        "content": user_question
    }
]


# -------------------
# CONTROLLER
# -------------------

def choose_action(json_objects):
    """
    Selects the next valid action.

    Important Day 5 improvement:
    - The controller avoids tools that already completed.
    - If the model repeats a completed tool, the controller chooses the next missing tool.
    """

    # First, try to use a valid model-suggested action.
    for obj in json_objects:
        action = obj.get("action")

        if action in required_tools and action not in tool_results:
            return obj

        if action == "final":
            return obj

    # Fallback: if the model fails or repeats itself,
    # the controller chooses the next missing required tool.
    for tool in required_tools:
        if tool not in tool_results:

            if tool == "current_date":
                return {
                    "thought": "Current date is still missing.",
                    "action": "current_date",
                    "input": ""
                }

            if tool == "calculator":
                return {
                    "thought": "Calculator result is still missing.",
                    "action": "calculator",
                    "input": "0.25 * 8400"
                }

    return {
        "thought": "All required tools are complete.",
        "action": "final",
        "answer": "done"
    }


# -------------------
# MEMORY FUNCTIONS
# -------------------

def retrieve_memory(memory_items):
    """
    Retrieves memory for the current task.

    For Day 5, memory is simple list-based memory.
    Later this will evolve into vector database retrieval.
    """

    if not memory_items:
        return "No memory available yet."

    return "\n".join(memory_items)


def update_memory(memory_store, item):
    """
    Adds useful information to memory.

    Duplicate memories are ignored to keep memory clean.
    """

    if item not in memory_store:
        memory_store.append(item)


# -------------------
# MEMORY-AWARE REACT LOOP
# -------------------

for step in range(MAX_STEPS):

    print(f"\n--- STEP {step + 1} ---")

    # Retrieve only recent memory to avoid overloading the small local model.
    retrieved_memory = retrieve_memory(memory_store[-3:])

    # Add memory and current workflow state into the conversation.
    messages.append({
        "role": "user",
        "content": f"""
Relevant memory:
{retrieved_memory}

Current observations:
{tool_results}

Thought history:
{thought_history}

Continue solving the original question:
{user_question}

Return exactly one JSON object.
"""
    })

    # Ask the model what to do next.
    decision_text = call_ollama(messages)

    print("MODEL OUTPUT:")
    print(decision_text)

    # Extract structured JSON from model output.
    json_objects = extract_json_objects(decision_text)

    # Controller decides the next valid action.
    decision = choose_action(json_objects)

    if not decision:
        print("No valid action found.")
        break

    thought = decision.get("thought", "")
    action = decision.get("action")
    tool_input = decision.get("input", "")

    print("\nTHOUGHT:")
    print(thought)

    thought_history.append(thought)

    # Stop if the model/controller says final.
    if action == "final":
        print("\nFINAL ANSWER:")
        print(decision.get("answer"))
        break

    # Execute tool if action is valid.
    if action in TOOLS:

        print(f"\nACTION: {action}")
        print("INPUT:", tool_input)

        try:
            if action == "current_date":
                result = TOOLS[action]()
            else:
                result = TOOLS[action](tool_input)

        except Exception as e:
            result = f"ERROR: {e}"

        print("\nOBSERVATION:")
        print(result)

        # Store successful observations in both tool_results and memory.
        if not result.startswith("ERROR"):
            tool_results[action] = result

            memory_item = f"Tool {action} returned: {result}"
            update_memory(memory_store, memory_item)

        # Store failed observations in memory too.
        else:
            memory_item = f"Tool {action} failed with input {tool_input}: {result}"
            update_memory(memory_store, memory_item)

        # Stop when all required tools have completed successfully.
        if all(tool in tool_results for tool in required_tools):
            break

    else:
        print("Invalid action:", action)
        break


# -------------------
# FINAL SUMMARY
# -------------------

print("\n--- FINAL STATE ---")

print("\nTOOL RESULTS:")
print(tool_results)

print("\nTHOUGHT HISTORY:")
for i, thought in enumerate(thought_history, start=1):
    print(f"{i}. {thought}")

print("\nMEMORY STORE:")
for i, item in enumerate(memory_store, start=1):
    print(f"{i}. {item}")

if "current_date" in tool_results and "calculator" in tool_results:
    print(
        f"\nFINAL CONTROLLER ANSWER:\n"
        f"Today is {tool_results['current_date']}.\n"
        f"25% of 8400 is {tool_results['calculator']}."
    )
else:
    print("\nAgent did not complete all required tools.")