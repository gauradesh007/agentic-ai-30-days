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
# AGENT REGISTRY
# -------------------

AGENT_REGISTRY = {
    "date_agent": date_agent,
    "math_agent": math_agent,
    "text_agent": text_agent,
}


# -------------------
# AGENT ROLES
# -------------------

AGENT_ROLES = {
    "date_agent": "Date Specialist",
    "math_agent": "Calculation Specialist",
    "text_agent": "Text Specialist",
}


# -------------------
# COLLABORATION STATE
# -------------------

collaboration_history = []


# -------------------
# CONTRIBUTION STATE
# -------------------

contribution_history = []


# -------------------
# SHARED GOAL STATE
# -------------------

shared_goal = (
    "Create a collaborative report using date, " "calculation, and text analysis."
)


# -------------------
# AGENT COLLABORATION
# -------------------


def collaborate(
    requesting_agent: str,
    helper_agent: str,
    goal: str,
) -> str:
    """
    Simulates collaboration between two agents.

    Responsibilities:
    - announce collaboration
    - execute the helper agent
    - capture the helper agent's role
    - record collaboration history
    - record contribution history
    """

    print(f"{requesting_agent} collaborates with " f"{helper_agent} on goal: {goal}")

    result = AGENT_REGISTRY[helper_agent]()

    role = AGENT_ROLES.get(
        helper_agent,
        "Unknown Role",
    )

    collaboration_history.append(
        {
            "requesting_agent": requesting_agent,
            "helper_agent": helper_agent,
            "role": role,
            "goal": goal,
            "result": result,
        }
    )

    contribution_history.append(
        {
            "agent": helper_agent,
            "role": role,
            "goal": goal,
            "contribution": result,
        }
    )

    return result


# -------------------
# LEAD AGENT
# -------------------


def lead_agent() -> str:
    """
    Lead agent responsible for producing the final collaborative report.

    The lead agent works with specialist agents toward one shared goal.
    """

    date_result = collaborate(
        "lead_agent",
        "date_agent",
        shared_goal,
    )

    math_result = collaborate(
        "lead_agent",
        "math_agent",
        shared_goal,
    )

    text_result = collaborate(
        "lead_agent",
        "text_agent",
        shared_goal,
    )

    return (
        "Collaborative Report\n\n"
        f"Shared Goal: {shared_goal}\n\n"
        f"Date: {date_result}\n"
        f"Calculation: {math_result}\n"
        f"Text Length: {text_result}"
    )


# -------------------
# EXECUTION
# -------------------

result = lead_agent()

print("\nFINAL REPORT:")
print(result)


# -------------------
# COLLABORATION SUMMARY
# -------------------

print("\nCOLLABORATION HISTORY:")

for i, item in enumerate(collaboration_history, start=1):
    print(
        f"{i}. "
        f"{item['requesting_agent']} "
        f"<-> "
        f"{item['helper_agent']} "
        f"({item['role']}) "
        f"| goal: {item['goal']} "
        f"-> "
        f"{item['result']}"
    )


# -------------------
# CONTRIBUTION SUMMARY
# -------------------

print("\nCONTRIBUTION HISTORY:")

for i, item in enumerate(contribution_history, start=1):
    print(
        f"{i}. "
        f"{item['agent']} "
        f"({item['role']}) "
        f"| goal: {item['goal']} "
        f"-> "
        f"{item['contribution']}"
    )
