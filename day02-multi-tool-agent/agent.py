import json
import requests
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"


# -------------------
# TOOLS
# -------------------

def calculator(expression: str) -> str:
    try:
        expression = expression.strip()

        if "%" in expression and "*" not in expression and "/" not in expression:
            parts = expression.replace("%", "").split()
            if len(parts) == 2:
                expression = f"{parts[0]}/100 * {parts[1]}"

        expression = expression.replace("%", "/100")

        allowed = "0123456789+-*/(). "
        if not all(char in allowed for char in expression):
            return "Invalid expression"

        return str(eval(expression))

    except Exception as e:
        return str(e)


def current_date() -> str:
    return datetime.now().strftime("%A, %d %B %Y")


def text_length(text: str) -> str:
    return str(len(text))


TOOLS = {
    "calculator": calculator,
    "current_date": current_date,
    "text_length": text_length
}

TOOL_ALIASES = {
    "calculation": "calculator",
    "math": "calculator",
    "date": "current_date",
    "today": "current_date"
}

# -------------------
# OLLAMA CALL
# -------------------

def call_ollama(messages):

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
        timeout=300
    )

    response.raise_for_status()

    return response.json()["message"]["content"]

def choose_next_action(json_objects, tool_results):
    for obj in json_objects:
        action = obj.get("action")
        action = TOOL_ALIASES.get(action, action)

        if action in required_tools and action not in tool_results:
            obj["action"] = action
            return obj

    for tool in required_tools:
        if tool not in tool_results:
            if tool == "current_date":
                return {"action": "current_date", "input": ""}
            if tool == "calculator":
                return {"action": "calculator", "input": "0.18 * 4500"}

    return {"action": "final", "answer": "done"}    

# -------------------
# JSON CLEANER
# -------------------

def extract_json_objects(text: str):
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
                    pass

    return objects

# -------------------
# USER QUESTION
# -------------------

user_question = "What day is it today and what is 18% of 4500?"
required_tools = ["current_date", "calculator"]


messages = [
    {
        "role": "system",
        "content": """
You are an AI agent controller.

Available tools:

1. calculator
Use for math.
Input must be a plain math expression string.
Example:
{"action": "calculator", "input": "0.18 * 4500"}

2. current_date
Use for today's day/date.
Input must be an empty string.
Example:
{"action": "current_date", "input": ""}

3. text_length
Use for counting characters in text.
Input must be the exact text.
Example:
{"action": "text_length", "input": "Agentic"}

Rules:
- Return exactly ONE JSON object.
- Use only one tool per response.
- Use only these action values: calculator, current_date, text_length, final.
- After a tool observation, decide the next action.
- Never invent tool names.
- Never answer math yourself. Use calculator.
- Only use tools required by the original user question. Do not introduce unrelated tools.
"""
    },
    {
        "role": "user",
        "content": user_question
    }
]
# -------------------
# AGENT LOOP
# -------------------

MAX_STEPS = 5
tool_results = {}

for step in range(MAX_STEPS):

    print(f"\n--- STEP {step + 1} ---")

    decision_text = call_ollama(messages)

    print("MODEL OUTPUT:")
    print(decision_text)

    json_objects = extract_json_objects(decision_text)

    if not json_objects:
        print("No valid JSON found. Controller will choose next required tool.")

    decision = choose_next_action(json_objects, tool_results)

    action = decision.get("action")
    action = TOOL_ALIASES.get(action, action)

    if action == "final":
        break

    elif action in TOOLS:

        tool_input = decision.get("input", "")

        print(f"\nUSING TOOL: {action}")
        print("INPUT:", tool_input)

        try:
            if action == "current_date":
                result = TOOLS[action]()
            else:
                result = TOOLS[action](tool_input)
        except Exception as e:
            result = f"Tool execution error: {e}"

        print("TOOL RESULT:", result)

        tool_results[action] = result

        if all(tool in tool_results for tool in required_tools):
            break

        messages.append({
            "role": "assistant",
            "content": decision_text
        })

        messages.append({
            "role": "user",
            "content": f"""
Original user question: {user_question}

Actual tool results so far:
{tool_results}

Do not invent tool results.
Use only the next missing required tool.
Return exactly one JSON object.
"""
        })

    else:
        print("\nINVALID TOOL REQUESTED")
        print(action)
        break


print("\n--- CONTROLLER SUMMARY ---")

if "current_date" in tool_results and "calculator" in tool_results:
    print(
        f"Today is {tool_results['current_date']}. "
        f"18% of 4500 is {tool_results['calculator']}."
    )
else:
    print("Agent did not collect all required tool results.")
    print("Collected results:", tool_results)

