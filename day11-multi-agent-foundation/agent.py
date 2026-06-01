from datetime import datetime

# -------------------
# TOOL FUNCTIONS
# -------------------


def calculator(expression: str) -> str:
    """
    Executes a simple math expression.

    Example:
    "0.20 * 4000" -> "800.0"
    """

    try:
        expression = expression.strip()
        expression = expression.replace("%", "/100")

        allowed = "0123456789+-*/(). "

        if not all(char in allowed for char in expression):
            return "ERROR: Invalid expression"

        return str(eval(expression))

    except Exception as e:
        return f"ERROR: {e}"


def current_date(_: str = "") -> str:
    """
    Returns the real current system date.
    """

    return datetime.now().strftime("%A, %d %B %Y")


def text_length(text: str) -> str:
    """
    Returns the character count of input text.

    Example:
    "MultiAgent" -> "10"
    """

    return str(len(text))


# -------------------
# SPECIALIST AGENTS
# -------------------


def date_agent() -> str:
    """
    Specialist agent responsible for date-related tasks.

    Uses:
    current_date tool
    """

    return current_date()


def math_agent() -> str:
    """
    Specialist agent responsible for math-related tasks.

    Uses:
    calculator tool
    """

    return calculator("0.20 * 4000")


def text_agent() -> str:
    """
    Specialist agent responsible for text-related tasks.

    Uses:
    text_length tool
    """

    return text_length("MultiAgent")


def summary_agent(results: dict) -> str:
    """
    Specialist agent responsible for creating a final summary.

    This agent demonstrates agent-to-agent communication because it uses
    outputs created by date_agent, math_agent, and text_agent.
    """

    return (
        f"Today is {results['date']}. "
        f"20% of 4000 is {results['math']}. "
        f"The word MultiAgent has {results['text']} characters."
    )


# -------------------
# AGENT REGISTRY
# -------------------

AGENT_REGISTRY = {
    "date_agent": date_agent,
    "math_agent": math_agent,
    "text_agent": text_agent,
    "summary_agent": summary_agent,
}


# -------------------
# CONTROLLER ROUTING
# -------------------


def choose_agent(task: str) -> str | None:
    """
    Chooses the correct specialist agent for a task.

    This is the controller's routing function.
    """

    if task == "date":
        return "date_agent"

    if task == "math":
        return "math_agent"

    if task == "text":
        return "text_agent"

    if task == "summary":
        return "summary_agent"

    return None


# -------------------
# TASK PLAN
# -------------------

tasks = [
    "date",
    "math",
    "text",
    "summary",
]


# -------------------
# MULTI-AGENT EXECUTION
# -------------------

results = {}

for task in tasks:
    selected_agent = choose_agent(task)

    if selected_agent is None:
        print("No agent found for task:", task)
        continue

    print("\nTASK:", task)
    print("AGENT:", selected_agent)

    if selected_agent == "summary_agent":
        result = AGENT_REGISTRY[selected_agent](results)
    else:
        result = AGENT_REGISTRY[selected_agent]()

    print("RESULT:", result)

    results[task] = result


# -------------------
# FINAL SUMMARY
# -------------------

print("\n--- FINAL RESULTS ---")

for task, result in results.items():
    print(task, "->", result)
