from typing import Literal
from typing import TypedDict
from typing import cast
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
    revision_count: int
    human_decision: str
    human_rejection_count: int


# -------------------
# AGENT NODES
# -------------------


def research_agent(
    state: WorkflowState,
) -> dict:
    """
    Research specialist agent.

    Creates research content for the topic.
    """

    print("Research Agent")

    response = llm.invoke(f"Research {state['topic']} in 3 short sentences.")

    return {"research": response.content}


def writer_agent(
    state: WorkflowState,
) -> dict:
    """
    Writer specialist agent.

    Creates or revises a beginner-friendly draft.
    """

    print("Writer Agent")
    print("Calling LLM from Writer Agent...")
    if state["status"] == "needs_revision":
        prompt = (
            "Revise this explanation based on the review feedback.\n\n"
            "Draft:\n"
            + state["draft"]
            + "\n\nReview:\n"
            + state["review"]
            + "\n\nReturn exactly 3 short beginner-friendly bullet points."
        )
    else:
        prompt = (
            "Rewrite this research for beginners.\n"
            "Return exactly 3 short beginner-friendly bullet points:\n\n"
            + state["research"]
        )

    response = llm.invoke(prompt)
    print("Writer Agent completed")
    return {"draft": response.content}


def reviewer_agent(
    state: WorkflowState,
) -> dict:
    """
    Reviewer specialist agent.

    Reviews the draft and returns a strict
    routing decision.
    """

    print("Reviewer Agent")

    response = llm.invoke(
        "You are a strict reviewer.\n"
        "Review the explanation below.\n\n"
        "Return ONLY one word:\n"
        "APPROVED\n"
        "or\n"
        "NEEDS_REVISION\n\n"
        "Return APPROVED only if the explanation has exactly "
        "3 short beginner-friendly bullet points.\n"
        "Return NEEDS_REVISION if it is too long, unclear, "
        "or does not follow the required format.\n\n"
        "Explanation:\n" + state["draft"]
    )

    review_text = response.content.strip().upper()

    if review_text == "APPROVED":
        status = "approved"

    elif review_text == "NEEDS_REVISION":
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


def human_approval(
    state: WorkflowState,
) -> dict:
    """
    Real human approval step.

    The human reviewer manually decides
    whether to approve or reject the workflow.
    """

    print("\nHuman Approval Required")
    print("=" * 60)

    print("\nCurrent Status:")
    print(state["status"])

    print("\nDraft:")
    print(state["draft"])

    print("\nReview:")
    print(state["review"])

    decision = input("\nEnter decision (APPROVE / REJECT): ").strip().upper()

    if decision not in [
        "APPROVE",
        "REJECT",
    ]:
        decision = "REJECT"

    return {"human_decision": decision}


def route_after_human(
    state: WorkflowState,
) -> Literal["__end__", "track_human_rejection"]:
    """
    Routes workflow after human review.

    APPROVE
        → END

    REJECT
        → track_human_rejection
    """

    if state["human_decision"] == "APPROVE":
        return END

    return "track_human_rejection"


# -------------------
# ROUTING FUNCTION
# -------------------


def route_after_review(
    state: WorkflowState,
) -> Literal["increment_revision", "final_decision"]:
    """
    Routes the workflow after review.

    approved
        → final_decision

    needs_revision and revision_count < 1
        → increment_revision

    needs_revision and revision_count >= 1
        → final_decision
    """

    if state["status"] == "approved":
        return "final_decision"

    if state["revision_count"] >= 1:
        return "final_decision"

    return "increment_revision"


def track_human_rejection(
    state: WorkflowState,
) -> dict:
    """
    Tracks how many times the human reviewer
    rejected the workflow output.
    """

    print("Track Human Rejection")

    return {"human_rejection_count": state["human_rejection_count"] + 1}


def route_after_rejection_tracking(
    state: WorkflowState,
) -> Literal["writer_agent", "__end__"]:
    """
    Routes after tracking human rejection.

    If rejection limit is reached, end workflow.
    Otherwise, send back to writer.
    """

    if state["human_rejection_count"] >= 2:
        return END

    return "writer_agent"


# -------------------
# REVISION TRACKING NODE
# -------------------


def increment_revision(
    state: WorkflowState,
) -> dict:
    """
    Increments revision count before sending
    work back to the writer.
    """

    print("Increment Revision Count")

    return {"revision_count": state["revision_count"] + 1}


def final_decision(
    state: WorkflowState,
) -> dict:
    """
    Makes a final workflow decision.

    If the reviewer approved the draft,
    the workflow is completed successfully.

    If the revision limit was reached and
    the reviewer still wants changes, the
    workflow completes with review errors.
    """

    print("Final Decision Agent")

    if state["status"] == "approved":
        return {
            "status": "approved",
            "review": (state["review"] + "\n\nFinal Decision: Approved."),
        }

    return {
        "status": "completed_with_review_errors",
        "review": (
            state["review"] + "\n\nFinal Decision: Revision limit reached. "
            "Manual review required."
        ),
    }


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
    "research_agent",
    research_agent,
)

graph.add_node(
    "writer_agent",
    writer_agent,
)

graph.add_node(
    "reviewer_agent",
    reviewer_agent,
)

graph.add_node(
    "increment_revision",
    increment_revision,
)
graph.add_node(
    "final_decision",
    final_decision,
)
graph.add_node(
    "human_approval",
    human_approval,
)

graph.add_node(
    "track_human_rejection",
    track_human_rejection,
)
# -------------------
# GRAPH EDGES
# -------------------

graph.add_edge(
    START,
    "research_agent",
)

graph.add_edge(
    "research_agent",
    "writer_agent",
)

graph.add_edge(
    "writer_agent",
    "reviewer_agent",
)

graph.add_conditional_edges(
    "reviewer_agent",
    route_after_review,
    {
        "increment_revision": "increment_revision",
        "final_decision": "final_decision",
    },
)

graph.add_edge(
    "increment_revision",
    "writer_agent",
)

graph.add_edge(
    "final_decision",
    "human_approval",
)
graph.add_conditional_edges(
    "human_approval",
    route_after_human,
    {
        "track_human_rejection": "track_human_rejection",
        "__end__": END,
    },
)

graph.add_conditional_edges(
    "track_human_rejection",
    route_after_rejection_tracking,
    {
        "writer_agent": "writer_agent",
        "__end__": END,
    },
)

# -------------------
# COMPILE GRAPH
# -------------------

workflow = graph.compile()


# -------------------
# EXECUTE GRAPH
# -------------------

result = cast(
    WorkflowState,
    workflow.invoke(
        {
            "topic": "AI agents",
            "research": "",
            "draft": "",
            "review": "",
            "status": "not_started",
            "revision_count": 0,
            "human_decision": "",
            "human_rejection_count": 0,
        }
    ),
)

display_result(result)
