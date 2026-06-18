from datetime import date
from typing import TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

# -------------------
# LLM
# -------------------

llm = ChatOllama(
    model="llama3.2:1b",
)


# -------------------
# WORKFLOW STATE
# -------------------


class WorkflowState(TypedDict):
    """
    Shared workflow state.

    The state stores:
    - user question
    - selected tool
    - tool answer
    - validation review
    """

    question: str
    tool: str
    answer: str
    review: str


# -------------------
# TOOLS
# -------------------


def calculator_tool() -> str:
    """
    Calculates 25% of 400.

    This is intentionally simple for
    learning tool execution flow.
    """

    result = (25 / 100) * 400

    return f"25% of 400 is {result}"


def date_tool() -> str:
    """
    Returns today's system date.
    """

    return str(date.today())


# -------------------
# TOOL GUARD
# -------------------


def normalize_tool_choice(
    question: str,
    llm_tool: str,
) -> str:
    """
    Corrects the LLM tool choice using
    simple deterministic guard rules.
    """

    question = question.lower()
    llm_tool = llm_tool.lower()

    if "date" in question or "today" in question:
        return "date"

    if "%" in question or "percent" in question:
        return "calculator"

    return llm_tool


def validate_tool_result(
    question: str,
    tool: str,
) -> str:
    """
    Validates whether the selected tool
    matches the user question.
    """

    question = question.lower()
    tool = tool.lower()

    if ("date" in question or "today" in question) and tool == "date":
        return "Tool selection is valid."

    if ("%" in question or "percent" in question) and tool == "calculator":
        return "Tool selection is valid."

    return "Tool selection may be incorrect."


# -------------------
# TOOL SELECTION AGENT
# -------------------


def tool_selection_agent(
    state: WorkflowState,
) -> dict:
    """
    Uses the LLM to choose a tool.

    The LLM suggests a tool, then guard
    logic validates and corrects the choice.
    """

    print("Tool Selection Agent")

    response = llm.invoke(
        "You must choose ONE tool.\n\n"
        "Available tools:\n"
        "- calculator\n"
        "- date\n\n"
        f"Question: {state['question']}\n\n"
        "Return ONLY the tool name."
    )

    llm_tool = response.content.strip().lower()

    tool = normalize_tool_choice(
        state["question"],
        llm_tool,
    )

    return {"tool": tool}


# -------------------
# TOOL EXECUTION AGENT
# -------------------


def tool_execution_agent(
    state: WorkflowState,
) -> dict:
    """
    Executes the selected tool.
    """

    print("Tool Execution Agent")

    if state["tool"] == "calculator":
        answer = calculator_tool()

    elif state["tool"] == "date":
        answer = date_tool()

    else:
        answer = "No valid tool selected."

    return {"answer": answer}


# -------------------
# TOOL REVIEW AGENT
# -------------------


def tool_review_agent(
    state: WorkflowState,
) -> dict:
    """
    Reviews whether the selected tool
    matched the user question.
    """

    print("Tool Review Agent")

    review = validate_tool_result(
        state["question"],
        state["tool"],
    )

    return {"review": review}


# -------------------
# DISPLAY FUNCTION
# -------------------


def display_result(
    state: WorkflowState,
) -> None:
    """
    Displays workflow state in a readable format.
    """

    print("\nFINAL STATE")
    print("=" * 60)

    for key, value in state.items():
        print(f"\n{key.upper()}")
        print("-" * 40)
        print(value)


# -------------------
# BUILD GRAPH
# -------------------

graph = StateGraph(WorkflowState)

graph.add_node(
    "tool_selection_agent",
    tool_selection_agent,
)

graph.add_node(
    "tool_execution_agent",
    tool_execution_agent,
)

graph.add_node(
    "tool_review_agent",
    tool_review_agent,
)


# -------------------
# GRAPH EDGES
# -------------------

graph.add_edge(
    START,
    "tool_selection_agent",
)

graph.add_edge(
    "tool_selection_agent",
    "tool_execution_agent",
)

graph.add_edge(
    "tool_execution_agent",
    "tool_review_agent",
)

graph.add_edge(
    "tool_review_agent",
    END,
)


# -------------------
# COMPILE GRAPH
# -------------------

workflow = graph.compile()


# -------------------
# EXECUTE GRAPH
# -------------------

result = workflow.invoke(
    {
        "question": "What is today's date?",
        "tool": "",
        "answer": "",
        "review": "",
    }
)


# -------------------
# DISPLAY RESULT
# -------------------

display_result(result)
