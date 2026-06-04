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
# TEAM GOAL
# -------------------

team_goal = "Create a team report using date, " "calculation, and text analysis."


# -------------------
# TEAM STATE
# -------------------

team_history = []

team_performance = {
    "team": "research_team",
    "goal": team_goal,
    "total_members": 0,
    "completed": 0,
    "failed": 0,
    "status": "not_started",
}


# -------------------
# AGENT TEAMS
# -------------------

AGENT_TEAMS = {
    "research_team": [
        "date_agent",
        "math_agent",
        "text_agent",
        # Intentional invalid member to demonstrate team validation.
        "unknown_agent",
    ]
}


# -------------------
# TEAM VALIDATION
# -------------------


def validate_team_member(member: str) -> bool:
    """
    Validates whether a team member exists in the agent registry.

    This prevents the team workflow from crashing when the team
    contains an unknown or unavailable member.
    """

    return member in AGENT_REGISTRY


# -------------------
# TEAM EXECUTION
# -------------------


def run_team(team_name: str) -> dict:
    """
    Executes all agents belonging to a team.

    Responsibilities:
    - load team members
    - validate each team member
    - execute valid members
    - record failed members
    - update team performance
    - record team history
    """

    members = AGENT_TEAMS.get(team_name, [])
    team_results = {}

    team_performance["total_members"] = len(members)
    team_performance["status"] = "running"

    for member in members:
        print(f"{team_name} executes {member}")

        if not validate_team_member(member):
            result = f"ERROR: Unknown team member: {member}"
            status = "failed"
            team_performance["failed"] += 1

        else:
            try:
                result = AGENT_REGISTRY[member]()
                status = "success"
                team_performance["completed"] += 1

            except Exception as e:
                result = f"ERROR: {e}"
                status = "failed"
                team_performance["failed"] += 1

        team_results[member] = result

        team_history.append(
            {
                "team": team_name,
                "goal": team_goal,
                "member": member,
                "role": AGENT_ROLES.get(member, "Unknown Role"),
                "status": status,
                "result": result,
            }
        )

    if team_performance["failed"] > 0:
        team_performance["status"] = "completed_with_errors"
    else:
        team_performance["status"] = "completed"

    return team_results


# -------------------
# TEAM LEADER
# -------------------


def team_leader() -> str:
    """
    Team leader responsible for managing the research team.

    It executes the team, collects member results,
    and produces the final team report.
    """

    results = run_team("research_team")

    return (
        "Team Report\n\n"
        f"Team Goal: {team_goal}\n\n"
        f"Date: {results['date_agent']}\n"
        f"Calculation: {results['math_agent']}\n"
        f"Text Length: {results['text_agent']}\n"
        f"Invalid Member Test: {results['unknown_agent']}"
    )


# -------------------
# FINAL TEAM DECISION
# -------------------


def final_team_decision() -> str:
    """
    Makes a final decision based on team performance.

    The team can:
    - complete successfully
    - complete with errors
    - fail completely
    """

    if team_performance["failed"] == 0:
        return "Team completed successfully."

    if team_performance["completed"] > 0 and team_performance["failed"] > 0:
        return "Team completed with errors. Review failed team members."

    return "Team failed. No members completed successfully."


# -------------------
# EXECUTION
# -------------------

report = team_leader()
team_decision = final_team_decision()

print("\nFINAL TEAM REPORT:")
print(report)


# -------------------
# TEAM HISTORY SUMMARY
# -------------------

print("\nTEAM HISTORY:")

for i, item in enumerate(team_history, start=1):
    print(
        f"{i}. "
        f"{item['team']} -> "
        f"{item['member']} "
        f"({item['role']}) | "
        f"status: {item['status']} | "
        f"goal: {item['goal']} | "
        f"result: {item['result']}"
    )


# -------------------
# TEAM PERFORMANCE SUMMARY
# -------------------

print("\nTEAM PERFORMANCE:")
print("Team:", team_performance["team"])
print("Goal:", team_performance["goal"])
print("Total members:", team_performance["total_members"])
print("Completed:", team_performance["completed"])
print("Failed:", team_performance["failed"])
print("Status:", team_performance["status"])


# -------------------
# FINAL TEAM DECISION SUMMARY
# -------------------

print("\nFINAL TEAM DECISION:")
print(team_decision)
