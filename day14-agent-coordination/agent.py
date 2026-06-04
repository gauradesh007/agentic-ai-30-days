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
# COORDINATION STATE
# -------------------

coordination_history = []
completed_agents = []


# -------------------
# WORKFLOW STATUS STATE
# -------------------

workflow_status = {
    "total_agents": 0,
    "completed": 0,
    "failed": 0,
    "status": "not_started",
}


# -------------------
# COORDINATION VALIDATION
# -------------------


def validate_coordination(helper_agent: str) -> bool:
    """
    Validates whether the helper agent exists before coordination.

    This prevents the coordinator from attempting to run
    an unknown or unavailable agent.
    """

    return helper_agent in AGENT_REGISTRY


# -------------------
# AGENT COORDINATION
# -------------------


def coordinate(
    coordinator: str,
    helper_agent: str,
) -> str:
    """
    Coordinates execution of a helper agent.

    Responsibilities:
    - announce coordination
    - validate helper agent
    - execute helper agent when valid
    - record success or failure
    - update workflow status counters
    """

    print(f"{coordinator} coordinates {helper_agent}")

    if not validate_coordination(helper_agent):
        result = f"ERROR: Unknown agent: {helper_agent}"

        workflow_status["failed"] += 1

        coordination_history.append(
            {
                "coordinator": coordinator,
                "agent": helper_agent,
                "role": "Unknown Role",
                "status": "failed",
                "result": result,
            }
        )

        return result

    result = AGENT_REGISTRY[helper_agent]()

    completed_agents.append(helper_agent)
    workflow_status["completed"] += 1

    coordination_history.append(
        {
            "coordinator": coordinator,
            "agent": helper_agent,
            "role": AGENT_ROLES.get(helper_agent, "Unknown Role"),
            "status": "success",
            "result": result,
        }
    )

    return result


# -------------------
# COORDINATOR AGENT
# -------------------


def coordinator_agent() -> str:
    """
    Coordinator agent responsible for managing the workflow.

    It controls:
    - execution order
    - agent validation
    - completion tracking
    - failure tracking
    - final report generation
    """

    workflow_status["total_agents"] = 4
    workflow_status["status"] = "running"

    date_result = coordinate(
        "coordinator_agent",
        "date_agent",
    )

    math_result = coordinate(
        "coordinator_agent",
        "math_agent",
    )

    text_result = coordinate(
        "coordinator_agent",
        "text_agent",
    )

    # Intentional invalid agent to demonstrate coordination validation.
    invalid_result = coordinate(
        "coordinator_agent",
        "unknown_agent",
    )

    if workflow_status["failed"] > 0:
        workflow_status["status"] = "completed_with_errors"
    else:
        workflow_status["status"] = "completed"

    return (
        "Coordinated Report\n\n"
        f"Date: {date_result}\n"
        f"Calculation: {math_result}\n"
        f"Text Length: {text_result}\n"
        f"Invalid Agent Test: {invalid_result}"
    )


# -------------------
# COORDINATOR FINAL DECISION
# -------------------


def coordinator_final_decision() -> str:
    """
    Makes a final decision based on workflow status.

    The coordinator classifies the workflow as:
    - completed successfully
    - completed with errors
    - failed
    """

    if workflow_status["failed"] == 0:
        return "Workflow completed successfully."

    if workflow_status["completed"] > 0 and workflow_status["failed"] > 0:
        return "Workflow completed with errors. " "Review failed agent coordination."

    return "Workflow failed. No agents completed successfully."


# -------------------
# EXECUTION
# -------------------

result = coordinator_agent()
final_decision = coordinator_final_decision()

print("\nFINAL REPORT:")
print(result)


# -------------------
# COORDINATION SUMMARY
# -------------------

print("\nCOORDINATION HISTORY:")

for i, item in enumerate(coordination_history, start=1):
    print(
        f"{i}. "
        f"{item['coordinator']} -> "
        f"{item['agent']} "
        f"({item['role']}) | "
        f"status: {item['status']} | "
        f"result: {item['result']}"
    )


# -------------------
# COMPLETION SUMMARY
# -------------------

print("\nCOMPLETED AGENTS:")

for agent in completed_agents:
    print("-", agent)


# -------------------
# WORKFLOW STATUS SUMMARY
# -------------------

print("\nWORKFLOW STATUS:")
print("Total agents:", workflow_status["total_agents"])
print("Completed:", workflow_status["completed"])
print("Failed:", workflow_status["failed"])
print("Status:", workflow_status["status"])


# -------------------
# FINAL DECISION SUMMARY
# -------------------

print("\nCOORDINATOR FINAL DECISION:")
print(final_decision)
