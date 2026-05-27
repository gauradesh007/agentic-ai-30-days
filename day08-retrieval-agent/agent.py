import json
import requests
from datetime import datetime

# Local Ollama API endpoint and model.
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"


# -------------------
# TOOL FUNCTIONS
# -------------------


def calculator(expression: str) -> str:
    """
    Executes a simple math expression.

    Example:
    "0.15 * 5000" -> "750.0"
    """

    try:
        expression = expression.strip()
        expression = expression.replace("%", "/100")

        # Basic safety check before using eval.
        allowed = "0123456789+-*/(). "

        if not all(char in allowed for char in expression):
            return "ERROR: Invalid expression"

        return str(eval(expression))

    except Exception as e:
        return f"ERROR: {e}"


def current_date(_: str = "") -> str:
    """
    Returns the real current system date.

    The unused input keeps all tool functions consistent:
    every tool accepts one string argument.
    """

    return datetime.now().strftime("%A, %d %B %Y")


def text_length(text: str) -> str:
    """
    Returns the character count of input text.

    Example:
    "Agentic" -> "7"
    """

    return str(len(text))


# -------------------
# TOOL REGISTRY
# -------------------

TOOL_REGISTRY = {
    "calculator": {
        "function": calculator,
        "description": "Performs math calculations.",
        "example": "0.15 * 5000",
    },
    "current_date": {
        "function": current_date,
        "description": "Returns today's date.",
        "example": "",
    },
    "text_length": {
        "function": text_length,
        "description": "Counts text characters.",
        "example": "Agentic",
    },
}


# -------------------
# MEMORY DATABASE
# -------------------

MEMORY_DB = [
    {
        "topic": "math",
        "content": "Percentage calculations should use decimal multiplication.",
    },
    {
        "topic": "date",
        "content": "current_date tool returns the real system date.",
    },
    {
        "topic": "text",
        "content": "text_length counts characters in a string.",
    },
]


# -------------------
# MEMORY RETRIEVAL
# -------------------


def retrieve_relevant_memory(question: str):
    """
    Retrieves relevant memory entries using simple keyword matching.

    This is a primitive retrieval system.
    Later this can evolve into embeddings, vector search, and RAG.
    """

    question = question.lower()
    results = []

    keyword_map = {
        "math": ["calculate", "calculation", "%", "percent", "percentage", "math"],
        "date": ["day", "date", "today", "current"],
        "text": ["character", "characters", "length", "text", "string"],
    }

    for item in MEMORY_DB:
        topic = item["topic"]
        keywords = keyword_map.get(topic, [])

        if any(keyword in question for keyword in keywords):
            results.append(item["content"])

    return results


# -------------------
# OLLAMA CALL
# -------------------


def call_ollama(messages):
    """
    Sends conversation history to Ollama and returns model response text.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0},
        },
        timeout=600,
    )

    response.raise_for_status()
    return response.json()["message"]["content"]


# -------------------
# JSON EXTRACTION
# -------------------


def extract_json_objects(text: str):
    """
    Extracts valid JSON objects from messy model output.

    Local models may return:
    - plain text
    - multiple JSON objects
    - malformed JSON
    - explanations outside JSON

    This function safely extracts usable JSON blocks.
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
                candidate = text[start : i + 1]

                try:
                    objects.append(json.loads(candidate))
                except:
                    pass

    return objects


# -------------------
# AGENT STATE
# -------------------

user_question = (
    "What day is it today, what is 15% of 5000, "
    "and how many characters are in Agentic?"
)

required_tools = [
    "current_date",
    "calculator",
    "text_length",
]

# Stores successful tool outputs.
tool_results = {}

# Stores model/controller reasoning traces.
thought_history = []

MAX_STEPS = 8

# Retrieve memory before the workflow starts.
retrieved_memory = retrieve_relevant_memory(user_question)


# -------------------
# SYSTEM PROMPT
# -------------------

messages = [
    {
        "role": "system",
        "content": f"""
You are a retrieval-aware AI workflow agent.

Relevant retrieved memory:
{retrieved_memory}

Available tools:
{list(TOOL_REGISTRY.keys())}

Always return EXACTLY ONE JSON object.

Format:

{{
  "thought": "reasoning",
  "action": "tool_name",
  "input": "tool input"
}}

OR

{{
  "thought": "reasoning",
  "action": "final",
  "answer": "final response"
}}

Rules:
- Use retrieved memory during reasoning
- Use one tool at a time
- Never explain outside JSON
""",
    },
    {
        "role": "user",
        "content": user_question,
    },
]


# -------------------
# CONTROLLER FUNCTIONS
# -------------------


def choose_action(json_objects):
    """
    Selects the first valid model action.

    Accepted actions:
    - registered tools
    - final response
    """

    for obj in json_objects:
        action = obj.get("action")

        if action in TOOL_REGISTRY:
            return obj

        if action == "final":
            return obj

    return None


def get_next_missing_tool(required_tools, tool_results):
    """
    Returns the next required tool that has not completed yet.
    """

    for tool in required_tools:
        if tool not in tool_results:
            return tool

    return None


def fallback_action_for_tool(tool_name):
    """
    Retrieval-aware controller fallback.

    Used when the model:
    - returns invalid output
    - selects a completed tool
    - selects the wrong tool
    - refuses incorrectly
    """

    if tool_name == "current_date":
        return {
            "thought": "Retrieved memory says current_date returns the real system date.",
            "action": "current_date",
            "input": "",
        }

    if tool_name == "calculator":
        return {
            "thought": "Retrieved memory says percentage calculations should use decimal multiplication.",
            "action": "calculator",
            "input": "0.15 * 5000",
        }

    if tool_name == "text_length":
        return {
            "thought": "Retrieved memory says text_length counts characters in a string.",
            "action": "text_length",
            "input": "Agentic",
        }

    return None


# -------------------
# RETRIEVAL-AWARE LOOP
# -------------------

for step in range(MAX_STEPS):
    print(f"\n--- STEP {step + 1} ---")

    # Re-retrieve memory each step.
    # In future versions, memory may change during execution.
    latest_retrieved_memory = retrieve_relevant_memory(user_question)

    # Give model current workflow state and retrieved memory.
    messages.append(
        {
            "role": "user",
            "content": f"""
Original question:
{user_question}

Retrieved memory:
{latest_retrieved_memory}

Required tools:
{required_tools}

Completed tool results:
{tool_results}

Thought history:
{thought_history}

Choose the next missing tool.
Use retrieved memory when deciding.
Return exactly one JSON object.
""",
        }
    )

    decision_text = call_ollama(messages)

    print("\nMODEL OUTPUT:")
    print(decision_text)

    json_objects = extract_json_objects(decision_text)
    decision = choose_action(json_objects)

    next_missing_tool = get_next_missing_tool(required_tools, tool_results)

    if not next_missing_tool:
        print("All required tools completed.")
        break

    # Use fallback if the model output is invalid.
    if not decision:
        print(
            "\nNo valid model action found. "
            "Controller will use retrieval-aware fallback."
        )
        decision = fallback_action_for_tool(next_missing_tool)

    if decision is None:
        break

    action = decision.get("action")
    thought = decision.get("thought", "")
    tool_input = decision.get("input", "")

    # Prevent repeated completed tools.
    if action in tool_results:
        print(
            f"\nTool {action} already completed. "
            "Controller will choose the next missing tool."
        )

        decision = fallback_action_for_tool(next_missing_tool)

        if decision is None:
            break

        action = decision.get("action")
        thought = decision.get("thought", "")
        tool_input = decision.get("input", "")

    # Enforce next expected tool.
    if action != next_missing_tool:
        print("\nACTION MISMATCH:")
        print(f"Expected next missing tool: {next_missing_tool}")
        print(f"Model selected: {action}")

        decision = fallback_action_for_tool(next_missing_tool)

        if decision is None:
            break

        action = decision.get("action")
        thought = decision.get("thought", "")
        tool_input = decision.get("input", "")

    print("\nRETRIEVED MEMORY:")
    for item in latest_retrieved_memory:
        print("-", item)

    print("\nTHOUGHT:")
    print(thought)

    thought_history.append(thought)

    if action == "final":
        break

    if action in TOOL_REGISTRY:
        print(f"\nACTION: {action}")
        print("INPUT:", tool_input)

        tool_function = TOOL_REGISTRY[action]["function"]

        try:
            result = tool_function(tool_input)
        except Exception as e:
            result = f"ERROR: {e}"

        print("\nOBSERVATION:")
        print(result)

        if not result.startswith("ERROR"):
            tool_results[action] = result
        else:
            print("Tool failed. Result not stored.")

    else:
        print("Invalid tool selected:", action)
        break


# -------------------
# FINAL SUMMARY
# -------------------

print("\n--- FINAL STATE ---")

print("\nRETRIEVED MEMORY:")
for item in retrieved_memory:
    print(f"- {item}")

print("\nTOOL RESULTS:")
print(tool_results)

print("\nTHOUGHT HISTORY:")
for i, thought in enumerate(thought_history, start=1):
    print(f"{i}. {thought}")

if all(tool in tool_results for tool in required_tools):
    print(
        f"\nFINAL CONTROLLER ANSWER:\n"
        f"Today is {tool_results['current_date']}.\n"
        f"15% of 5000 is {tool_results['calculator']}.\n"
        f"The word Agentic has {tool_results['text_length']} characters."
    )
else:
    print("\nAgent did not complete all required tools.")
