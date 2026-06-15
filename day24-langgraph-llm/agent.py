from typing import Literal
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
    topic: str
    research: str
    draft: str
    review: str
    status: str


# -------------------
# RESEARCH NODE
# -------------------


def research_node(
    state: WorkflowState,
):
    """
    Researches the topic using the LLM.
    """

    print("Executing research node")

    response = llm.invoke(f"Explain {state['topic']} " "in 3 short sentences.")

    return {"research": response.content}


# -------------------
# WRITER NODE
# -------------------


def writer_node(
    state: WorkflowState,
):
    """
    Converts research into a beginner-friendly explanation.
    """

    print("Executing writer node")

    response = llm.invoke(
        "Rewrite the following for beginners "
        "in 3 short bullet points:\n\n" + state["research"]
    )

    return {"draft": response.content}


# -------------------
# REVIEW NODE
# -------------------


def review_node(
    state: WorkflowState,
):
    """
    Reviews the draft and returns a strict routing decision.

    The LLM must return only:
    - APPROVED
    - NEEDS_REVISION
    """

    print("Executing review node")

    response = llm.invoke(
        "You are a strict reviewer.\n"
        "Review the explanation below.\n\n"
        "Return ONLY one word:\n"
        "APPROVED\n"
        "or\n"
        "NEEDS_REVISION\n\n"
        "Return APPROVED only if the explanation is clear, short, "
        "and beginner-friendly.\n"
        "Return NEEDS_REVISION if it is too long, unclear, or needs improvement.\n\n"
        "Explanation:\n" + state["draft"]
    )

    review_text = response.content.strip().upper()

    if "APPROVED" == review_text:
        status = "approved"

    elif "NEEDS_REVISION" == review_text:
        status = "needs_revision"

    else:
        status = "needs_revision"
        review_text = (
            "NEEDS_REVISION " "(Reviewer did not return a valid strict decision.)"
        )

    return {
        "review": review_text,
        "status": status,
    }


# -------------------
# REVISE NODE
# -------------------


def revise_node(
    state: WorkflowState,
):
    """
    Revises the draft if the review requires improvement.
    """

    print("Executing revise node")

    response = llm.invoke(
        "Revise this explanation.\n"
        "Make it exactly 3 short beginner-friendly bullet points.\n\n"
        "Original explanation:\n" + state["draft"]
    )

    return {
        "draft": response.content,
        "review": "Revision completed.",
        "status": "approved",
    }


# -------------------
# ROUTING FUNCTION
# -------------------


def route_after_review(
    state: WorkflowState,
) -> Literal["revise_node", "__end__"]:
    """
    Routes the workflow after review.

    approved
        → END

    needs_revision
        → revise_node
    """

    if state["status"] == "approved":
        return END

    return "revise_node"


# -------------------
# BUILD GRAPH
# -------------------

graph = StateGraph(WorkflowState)

graph.add_node(
    "research_node",
    research_node,
)

graph.add_node(
    "writer_node",
    writer_node,
)

graph.add_node(
    "review_node",
    review_node,
)

graph.add_node(
    "revise_node",
    revise_node,
)


# -------------------
# GRAPH EDGES
# -------------------

graph.add_edge(
    START,
    "research_node",
)

graph.add_edge(
    "research_node",
    "writer_node",
)

graph.add_edge(
    "writer_node",
    "review_node",
)

graph.add_conditional_edges(
    "review_node",
    route_after_review,
)

graph.add_edge(
    "revise_node",
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
        "topic": "AI agents",
        "research": "",
        "draft": "",
        "review": "",
        "status": "not_started",
    }
)

print("\nFINAL STATE:")
print(result)
