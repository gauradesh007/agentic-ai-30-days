import json
import requests
from datetime import datetime

# Ollama runs locally on this URL.
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"


# -------------------
# TOOLS
# -------------------

def calculator(expression: str) -> str:
    """
    Executes a math expression safely for this learning project.

    Example:
    "0.15 * 9600" -> "1440.0"
    """

    try:
        expression = expression.strip()

        # Convert inputs like "15% 9600" into "15/100 * 9600"
        if "%" in expression and "*" not in expression and "/" not in expression:
            parts = expression.replace("%", "").split()

            if len(parts) == 2:
                expression = f"{parts[0]}/100 * {parts[1]}"

        # Convert "15%" into "15/100"
        expression = expression.replace("%", "/100")

        # Basic safety check before eval.
        allowed = "0123456789+-*/(). "

        if not all(char in allowed for char in expression):
            return "ERROR: Invalid expression"

        return str(eval(expression))

    except Exception as e:
        return f"ERROR: {e}"


def current_date() -> str:
    """
    Returns the actual current system date.
    This prevents the LLM from hallucinating dates.
    """
    return datetime.now().strftime("%A, %d %B %Y")


# Tool registry: controller can dynamically call tools by name.
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
        timeout=300
    )

    response.raise_for_status()
    return response.json()["message"]["content"]


# -------------------
# JSON EXTRACTION
# -------------------

def extract_json_objects(text: str):
    """
    Extracts valid JSON objects from messy LLM output.

    The local model may return explanations plus JSON.
    This function scans the response and extracts usable JSON blocks.
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
                    pass

    return objects


# -------------------
# AGENT STATE
# -------------------

user_question = "What day is it today and what is 15% of 9600?"

# These are the tools required to fully answer the question.
required_tools = ["current_date", "calculator"]

# Stores successful tool outputs.
tool_results = {}

# Stores model thoughts for later inspection.
thought_history = []

# Stores failed tool attempts.
failure_history = []

MAX_STEPS = 6


# -------------------
# SYSTEM PROMPT
# -------------------

messages = [
    {
        "role": "system",
        "content": """
You are a ReAct-style AI workflow agent.

You must reason step-by-step.

Always return EXACTLY ONE JSON object.

Format:

{
  "thought": "your reasoning",
  "action": "tool_name",
  "input": "tool input"
}

OR

{
  "thought": "your reasoning",
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
- Tool inputs must be plain executable values
- Never wrap calculator expressions inside JSON
"""
    },
    {
        "role": "user",
        "content": user_question
    }
]


# -------------------
# CONTROLLER FUNCTIONS
# -------------------

def choose_action(json_objects):
    """
    Selects the first valid action suggested by the model.

    The model may return multiple JSON objects or invalid ones.
    The controller only accepts:
    - required tools
    - final response
    """

    for obj in json_objects:
        action = obj.get("action")

        if action in required_tools:
            return obj

        if action == "final":
            return obj

    return None


def validate_calculator_input(expression: str) -> bool:
    """
    Semantic validation for the calculator.

    The calculator may technically execute "9600",
    but that does not answer "15% of 9600".

    This function ensures the input actually represents
    the required percentage calculation.
    """

    expression = expression.strip()

    has_number = "9600" in expression

    has_percentage_logic = (
        "0.15" in expression
        or "15/100" in expression
        or "15%" in expression
    )

    return has_number and has_percentage_logic


# -------------------
# REACT AGENT LOOP
# -------------------

for step in range(MAX_STEPS):

    print(f"\n--- STEP {step + 1} ---")

    # Ask the model what to do next.
    decision_text = call_ollama(messages)

    print("MODEL OUTPUT:")
    print(decision_text)

    # Extract structured JSON from messy model output.
    json_objects = extract_json_objects(decision_text)

    # Controller chooses the next valid action.
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

    # If model says final, stop.
    if action == "final":
        print("\nFINAL ANSWER:")
        print(decision.get("answer"))
        break

    # Execute valid tools.
    if action in TOOLS:

        print(f"\nACTION: {action}")
        print("INPUT:", tool_input)

        try:
            if action == "current_date":
                result = TOOLS[action]()

            elif action == "calculator":
                if not validate_calculator_input(tool_input):
                    result = "ERROR: Calculator input does not match required percentage calculation"
                else:
                    result = TOOLS[action](tool_input)

            else:
                result = "ERROR: Unknown tool"

        except Exception as e:
            result = f"ERROR: {e}"

        print("\nOBSERVATION:")
        print(result)

        # Store failed attempts separately.
        if result.startswith("ERROR"):
            failure_history.append({
                "thought": thought,
                "action": action,
                "input": tool_input,
                "error": result
            })

        # Store only successful tool results.
        else:
            tool_results[action] = result

            # Stop once all required tools have succeeded.
            if all(tool in tool_results for tool in required_tools):
                break

        # Add observation back into the conversation.
        # This is the Observation step in ReAct.
        messages.append({
            "role": "assistant",
            "content": decision_text
        })

        messages.append({
            "role": "user",
            "content": f"""
Original question:
{user_question}

Observations so far:
{tool_results}

Failures:
{failure_history}

Thought history:
{thought_history}

For calculator, use the exact expression: 0.15 * 9600.
Do not use only 9600 as calculator input.

Continue using ReAct:
Think about what information is still missing.
Use only one next action.
Return exactly one JSON object.
"""
        })

    else:
        print("Invalid action:", action)
        break


# -------------------
# FINAL SUMMARY
# -------------------

print("\n--- FINAL STATE ---")

print("\nTOOL RESULTS:")
print(tool_results)

print("\nFAILURE HISTORY:")
print(failure_history)

print("\nTHOUGHT HISTORY:")
for i, thought in enumerate(thought_history, start=1):
    print(f"{i}. {thought}")

if "current_date" in tool_results and "calculator" in tool_results:
    print(
        f"\nFINAL CONTROLLER ANSWER:\n"
        f"Today is {tool_results['current_date']}.\n"
        f"15% of 9600 is {tool_results['calculator']}."
    )
else:
    print("\nAgent did not complete all required tools.")