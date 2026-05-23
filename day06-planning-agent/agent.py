import json
import requests
from datetime import datetime

# Local Ollama API endpoint and model.
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"


# -------------------
# TOOLS
# -------------------


def calculator(expression: str) -> str:
    """
    Executes a simple math expression.

    Example:
    "0.18 * 2500" -> "450.0"
    """

    try:
        expression = expression.strip()
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
    Returns the actual system date.
    This prevents the model from hallucinating today's date.
    """

    return datetime.now().strftime("%A, %d %B %Y")


# Tool registry.
TOOLS = {
    "calculator": calculator,
    "current_date": current_date,
}


# -------------------
# OLLAMA CALL
# -------------------


def call_ollama(messages):
    """
    Sends conversation history to Ollama and returns the model response.
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

    Local models may return extra text, multiple JSON blocks, or malformed text.
    This function extracts usable JSON objects safely.
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
# PLANNING STATE
# -------------------

user_question = "What day is it today and what is 18% of 2500?"

# Explicit plan state.
task_plan = []
completed_tasks = []

# Stores successful tool outputs.
tool_results = {}

# Stores reasoning traces.
thought_history = []

MAX_STEPS = 8


# -------------------
# SYSTEM PROMPT
# -------------------

messages = [
    {
        "role": "system",
        "content": """
You are a planning-based ReAct AI workflow agent.

You must:
- create plans
- execute tasks step-by-step
- update plans using observations
- think carefully before acting

Always return EXACTLY ONE JSON object.

Format:

{
  "thought": "reasoning",
  "task": "current task",
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
""",
    },
    {"role": "user", "content": user_question},
]


# -------------------
# CONTROLLER FUNCTIONS
# -------------------


def choose_action(json_objects):
    """
    Chooses the first valid model-suggested action.

    The controller only accepts:
    - known tools
    - final response
    """

    for obj in json_objects:
        action = obj.get("action")

        if action in TOOLS:
            return obj

        if action == "final":
            return obj

    return None


def create_initial_plan():
    """
    Creates the initial execution plan.

    Day 6 introduces explicit planning:
    planner → executor → observation → final summary
    """

    return [
        "Get current date",
        "Calculate 18% of 2500",
        "Generate final response",
    ]


def get_next_task(task_plan, completed_tasks):
    """
    Returns the next incomplete task from the plan.
    """

    for task in task_plan:
        if task not in completed_tasks:
            return task

    return None


def expected_action_for_task(task):
    """
    Maps each task to the tool/action that should execute it.

    This validates whether the model's action matches the current planned task.
    """

    task_lower = task.lower()

    if "date" in task_lower:
        return "current_date"

    if "calculate" in task_lower or "%" in task:
        return "calculator"

    if "final" in task_lower or "response" in task_lower:
        return "final"

    return None


def correct_action_for_task(expected_action):
    """
    Controller correction layer.

    If the model chooses the wrong action for the current task,
    the controller replaces it with the expected action.
    """

    if expected_action == "calculator":
        return {
            "thought": "The current task requires calculation, so the controller is correcting the action.",
            "action": "calculator",
            "input": "0.18 * 2500",
        }

    if expected_action == "current_date":
        return {
            "thought": "The current task requires today's date, so the controller is correcting the action.",
            "action": "current_date",
            "input": "",
        }

    if expected_action == "final":
        return {
            "thought": "All required observations are available, so the controller is generating final response.",
            "action": "final",
            "answer": "done",
        }

    return None


# -------------------
# CREATE INITIAL PLAN
# -------------------

task_plan = create_initial_plan()


# -------------------
# PLANNER-EXECUTOR LOOP
# -------------------

for step in range(MAX_STEPS):
    print(f"\n--- STEP {step + 1} ---")

    # Get next task from the explicit task plan.
    current_task = get_next_task(task_plan, completed_tasks)

    if not current_task:
        print("All tasks completed.")
        break

    # The final response is generated by the controller summary,
    # so we mark this task complete and stop asking the weak local model.
    if current_task == "Generate final response":
        completed_tasks.append(current_task)
        break

    print("\nCURRENT TASK:")
    print(current_task)

    # Give the model current planning context.
    messages.append(
        {
            "role": "user",
            "content": f"""
Current task:
{current_task}

Current plan:
{task_plan}

Completed tasks:
{completed_tasks}

Observations:
{tool_results}

Thought history:
{thought_history}

Generate the next correct action.
Return exactly one JSON object.
""",
        }
    )

    # Ask model for next action.
    decision_text = call_ollama(messages)

    print("\nMODEL OUTPUT:")
    print(decision_text)

    json_objects = extract_json_objects(decision_text)
    decision = choose_action(json_objects)

    if not decision:
        print("No valid action found.")
        break

    thought = decision.get("thought", "")
    action = decision.get("action")
    tool_input = decision.get("input", "")

    expected_action = expected_action_for_task(current_task)

    # Validate model action against the current planned task.
    if action != expected_action:
        print("\nACTION MISMATCH:")
        print(f"Expected: {expected_action}")
        print(f"Got: {action}")

        corrected_decision = correct_action_for_task(expected_action)

        if not corrected_decision:
            print("Controller could not correct the action.")
            break

        decision = corrected_decision
        thought = decision.get("thought", "")
        action = decision.get("action")
        tool_input = decision.get("input", "")

    print("\nTHOUGHT:")
    print(thought)

    thought_history.append(thought)

    # Execute valid tools.
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

        if not result.startswith("ERROR"):
            tool_results[action] = result

            if current_task not in completed_tasks:
                completed_tasks.append(current_task)

        else:
            print("Task failed. Plan will continue.")

    else:
        print("Invalid action:", action)
        break


# -------------------
# FINAL SUMMARY
# -------------------

print("\n--- FINAL STATE ---")

print("\nTASK PLAN:")
for i, task in enumerate(task_plan, start=1):
    print(f"{i}. {task}")

print("\nCOMPLETED TASKS:")
for i, task in enumerate(completed_tasks, start=1):
    print(f"{i}. {task}")

print("\nTOOL RESULTS:")
print(tool_results)

print("\nTHOUGHT HISTORY:")
for i, thought in enumerate(thought_history, start=1):
    print(f"{i}. {thought}")

if "current_date" in tool_results and "calculator" in tool_results:
    print(
        f"\nFINAL CONTROLLER ANSWER:\n"
        f"Today is {tool_results['current_date']}.\n"
        f"18% of 2500 is {tool_results['calculator']}."
    )
else:
    print("\nAgent did not complete all required tasks.")
