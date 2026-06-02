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
# DELEGATION STATE
# -------------------

delegation_history = []


# -------------------
# DELEGATION VALIDATION
# -------------------


def validate_delegation(to_agent: str) -> bool:
    """
    Validates whether the target agent exists before delegation.

    This prevents the workflow from crashing when an agent delegates
    to an unknown or unavailable agent.
    """

    return to_agent in AGENT_REGISTRY


# -------------------
# AGENT DELEGATION
# -------------------


def delegate_task(from_agent: str, to_agent: str) -> str:
    """
    Delegates work from one agent to another agent.

    Responsibilities:
    - validate the target agent
    - execute the target agent if valid
    - record delegation status
    - return the delegated result
    """

    print(f"{from_agent} delegates work to {to_agent}")

    if not validate_delegation(to_agent):
        result = f"ERROR: Cannot delegate to unknown agent: {to_agent}"

        delegation_history.append(
            {
                "from_agent": from_agent,
                "to_agent": to_agent,
                "status": "failed",
                "result": result,
            }
        )

        return result

    result = AGENT_REGISTRY[to_agent]()

    delegation_history.append(
        {
            "from_agent": from_agent,
            "to_agent": to_agent,
            "status": "success",
            "result": result,
        }
    )

    return result


# -------------------
# PRIMARY AGENT
# -------------------


def research_agent() -> str:
    """
    Primary agent responsible for creating a research-style report.

    The research_agent does not perform every task itself.
    Instead, it delegates specialized work to specialist agents.
    """

    date_result = delegate_task(
        "research_agent",
        "date_agent",
    )

    math_result = delegate_task(
        "research_agent",
        "math_agent",
    )

    text_result = delegate_task(
        "research_agent",
        "text_agent",
    )

    # Intentional invalid delegation to demonstrate validation.
    invalid_result = delegate_task(
        "research_agent",
        "unknown_agent",
    )

    return (
        "Research completed.\n"
        f"Date: {date_result}\n"
        f"Calculation: {math_result}\n"
        f"Text length: {text_result}\n"
        f"Invalid delegation test: {invalid_result}"
    )


# -------------------
# EXECUTION
# -------------------

result = research_agent()

print("\nFINAL RESULT:")
print(result)

print("\nDELEGATION HISTORY:")

for i, item in enumerate(delegation_history, start=1):
    print(
        f"{i}. {item['from_agent']} -> "
        f"{item['to_agent']} | "
        f"status: {item['status']} | "
        f"result: {item['result']}"
    )
