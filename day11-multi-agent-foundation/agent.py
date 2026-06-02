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

    The unused argument keeps the tool interface consistent.
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
    """

    return current_date()


def math_agent() -> str:
    """
    Specialist agent responsible for math-related tasks.
    """

    return calculator("0.20 * 4000")


def text_agent() -> str:
    """
    Specialist agent responsible for text-related tasks.
    """

    return text_length("MultiAgent")


# -------------------
# AGENT COMMUNICATION
# -------------------


def send_message(from_agent: str, to_agent: str, message: str) -> str:
    """
    Simulates a message sent from one agent to another.

    Day 11 uses simple string-based communication.
    Later this can evolve into structured messages or real agent protocols.
    """

    return f"{from_agent} asks {to_agent}: {message}"


# -------------------
# COORDINATOR AGENTS
# -------------------


def summary_agent(results: dict) -> str:
    """
    Creates a concise final summary using outputs from other agents.

    This demonstrates shared-result communication:
    date_agent, math_agent, and text_agent produce values,
    then summary_agent combines them.
    """

    return (
        f"Today is {results['date']}. "
        f"20% of 4000 is {results['math']}. "
        f"The word MultiAgent has {results['text']} characters."
    )


def report_agent(results: dict) -> str:
    """
    Creates a detailed report by simulating messages to other agents.

    This demonstrates agent-to-agent communication:
    report_agent requests information from math_agent and text_agent,
    then builds a report from their outputs.
    """

    message_to_math = send_message(
        "report_agent",
        "math_agent",
        "Please provide the calculation result.",
    )

    message_to_text = send_message(
        "report_agent",
        "text_agent",
        "Please provide the text analysis result.",
    )

    return (
        f"{message_to_math}\n"
        f"math_agent responded with: {results['math']}\n\n"
        f"{message_to_text}\n"
        f"text_agent responded with: {results['text']}\n\n"
        f"Final report: On {results['date']}, "
        f"20% of 4000 was {results['math']}, "
        f"and MultiAgent has {results['text']} characters."
    )


# -------------------
# AGENT REGISTRY
# -------------------

AGENT_REGISTRY = {
    "date_agent": date_agent,
    "math_agent": math_agent,
    "text_agent": text_agent,
    "summary_agent": summary_agent,
    "report_agent": report_agent,
}


# -------------------
# CONTROLLER ROUTING
# -------------------


def choose_agent(task: str) -> str | None:
    """
    Routes a task to the correct specialist or coordinator agent.

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

    if task == "report":
        return "report_agent"

    return None


# -------------------
# TASK PLAN
# -------------------

tasks = [
    "date",
    "math",
    "text",
    "summary",
    "report",
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

    # Coordinator agents need previous agent results.
    if selected_agent in ["summary_agent", "report_agent"]:
        result = AGENT_REGISTRY[selected_agent](results)

    # Specialist agents run independently.
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
