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
            return "ERROR: Invalid expression"

        return str(eval(expression))

    except Exception as e:
        return f"ERROR: {e}"


def current_date() -> str:
    return datetime.now().strftime("%A, %d %B %Y")


TOOLS = {
    "calculator": calculator,
    "current_date": current_date
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
# -------------------
# JSON EXTRACTION
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
# AGENT STATE
# -------------------

#user_question = "What day is it today and what is twenty two percent of 6200?"
user_question = "What day is it today and calculate twenty-two percent multiplied by sixty-two hundred dollars?"

required_tools = ["current_date", "calculator"]

tool_results = {}

failure_history = []

retry_count = {}

MAX_RETRIES = 2

# system Prompt

messages = [
    {
        "role": "system",
        "content": """
You are an AI workflow controller.

Available tools:
- calculator
- current_date

Rules:
- Return EXACTLY ONE JSON object
- Never explain outside JSON
- Use only valid tool names
- Use calculator for math
- Use current_date for today's date

Examples:

{"action": "calculator", "input": "0.22 * 6200"}


{"action": "current_date", "input": ""}

{"action": "final", "answer": "text"}
"""
    },
    {
        "role": "user",
        "content": user_question
    }
]
#STEP 8 — CONTROLLER FUNCTION

# -------------------
# CONTROLLER
# -------------------

def choose_action(json_objects):

    for obj in json_objects:

        action = obj.get("action")

        if action in required_tools:
            return obj

        if action == "final":
            return obj

    return None

#STEP 9 — MAIN LOOP
# -------------------
# AGENT LOOP
# -------------------

MAX_STEPS = 6

for step in range(MAX_STEPS):

    print(f"\n--- STEP {step + 1} ---")

    decision_text = call_ollama(messages)

    print("MODEL OUTPUT:")
    print(decision_text)

    json_objects = extract_json_objects(decision_text)

    decision = choose_action(json_objects)

    if not decision:

        print("No valid action found.")

        failure_history.append("No valid JSON action")

        continue

    action = decision.get("action")

    # FINAL ANSWER
    if action == "final":

        print("\nFINAL ANSWER:")
        print(decision.get("answer"))

        break

    # INVALID RETRY LIMIT
    if retry_count.get(action, 0) >= MAX_RETRIES:

        print(f"\nTOOL '{action}' exceeded retry limit.")

        failure_history.append(f"{action} exceeded retries")

        continue

    tool_input = decision.get("input", "")

    print(f"\nUSING TOOL: {action}")
    print("INPUT:", tool_input)

    # EXECUTE TOOL
    try:

        if action == "current_date":
            result = TOOLS[action]()

        else:
            result = TOOLS[action](tool_input)

    except Exception as e:

        result = f"ERROR: {e}"

    print("TOOL RESULT:", result)

    # FAILURE DETECTION
    if result.startswith("ERROR"):

        retry_count[action] = retry_count.get(action, 0) + 1

        failure_history.append({
            "tool": action,
            "input": tool_input,
            "error": result
        })

        print(f"RETRY COUNT: {retry_count[action]}")

    else:

        tool_results[action] = result

    # STOP CONDITION
    if all(tool in tool_results for tool in required_tools):

        break

    # OBSERVATION
    messages.append({
        "role": "assistant",
        "content": decision_text
    })

    messages.append({
        "role": "user",
        "content": f"""
Original question:
{user_question}

Successful results:
{tool_results}

Failures:
{failure_history}

Avoid repeating failed actions.
Use only missing required tools.
Return exactly one JSON object.
"""
    })

# STEP 10 — FINAL SUMMARY   
# -------------------
# FINAL SUMMARY
# -------------------

print("\n--- FINAL STATE ---")

print("\nTOOL RESULTS:")
print(tool_results)

print("\nFAILURE HISTORY:")
print(failure_history)

print("\nRETRY COUNTS:")
print(retry_count)

if all(tool in tool_results for tool in required_tools):
    print(
        f"\nFINAL CONTROLLER ANSWER:\n"
        f"Today is {tool_results['current_date']}.\n"
        f"22% of 6200 is {tool_results['calculator']}."
    )
else:
    print("\nAgent could not fully complete the task.")
