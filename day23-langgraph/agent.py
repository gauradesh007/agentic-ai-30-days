from typing import Literal
from typing import TypedDict

from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

# -------------------
# WORKFLOW STATE
# -------------------


class WorkflowState(TypedDict):
    """
    Shared workflow state.

    The state is passed between graph nodes
    and updated as the workflow progresses.
    """

    message: str
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
    Creates research content.

    Updates:
    - research
    """

    print("Executing research node")

    return {
        "research": ("AI agents can reason, act, " "and use tools to complete goals.")
    }


# -------------------
# WRITE NODE
# -------------------


def write_node(
    state: WorkflowState,
):
    """
    Creates a draft using research.

    This version intentionally omits the
    word 'Beginner' so the review node
    forces the revision path.
    """

    print("Executing write node")

    return {"draft": ("Explanation: " + state["research"])}


# -------------------
# REVIEW NODE
# -------------------


def review_node(
    state: WorkflowState,
):
    """
    Reviews the draft.

    If the draft contains the word
    'Beginner', it is approved.

    Otherwise it requires revision.
    """

    print("Executing review node")

    if "Beginner" in state["draft"]:
        return {
            "review": ("Review complete. " "Draft is clear and accurate."),
            "status": "approved",
        }

    return {
        "review": "Draft needs revision.",
        "status": "needs_revision",
    }


# -------------------
# REVISION NODE
# -------------------


def revise_node(
    state: WorkflowState,
):
    """
    Revises the draft when review fails.

    Updates:
    - draft
    - review
    - status
    """

    print("Executing revise node")

    return {
        "draft": (state["draft"] + " Revised for clarity."),
        "review": "Revision complete.",
        "status": "approved",
    }


# -------------------
# ROUTING FUNCTION
# -------------------


def route_after_review(
    state: WorkflowState,
) -> Literal["revise_node", "__end__"]:
    """
    Determines the next step after review.

    Routing logic:

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
    "write_node",
    write_node,
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

# START
#   ↓
# research_node
#   ↓
# write_node
#   ↓
# review_node
#   ↓
# approved      → END
# needs_revision → revise_node → END

graph.add_edge(
    START,
    "research_node",
)

graph.add_edge(
    "research_node",
    "write_node",
)

graph.add_edge(
    "write_node",
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
        "message": "Explain AI agents",
        "research": "",
        "draft": "",
        "review": "",
        "status": "not_started",
    }
)


# -------------------
# DISPLAY RESULTS
# -------------------

print("\nFINAL STATE:")
print(result)
