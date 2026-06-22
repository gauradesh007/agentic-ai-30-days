import chromadb

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
# CHROMADB KNOWLEDGE BASE
# -------------------

client = chromadb.Client()

collection = client.get_or_create_collection(name="retrieved_knowledge")

collection.add(
    documents=[
        "Percentage calculations use decimal multiplication.",
        "Current date returns the real system date.",
        "Text length counts characters in a string.",
    ],
    ids=[
        "math",
        "date",
        "text",
    ],
)


# -------------------
# WORKFLOW STATE
# -------------------


class WorkflowState(TypedDict):
    """
    Shared workflow state for the end-to-end agent.

    Stores:
    - question
    - retrieved knowledge
    - tool result
    - generated answer
    - review result
    - revision count
    - final status
    - human decision
    """

    question: str
    retrieved_knowledge: str
    tool_result: str
    answer: str
    review: str
    revision_count: int
    status: str
    human_decision: str


# -------------------
# TOOL
# -------------------


def calculator_tool() -> str:
    """
    Performs a sample percentage calculation.
    """

    result = (25 / 100) * 400

    return f"Tool result: 25% of 400 is {result}."


# -------------------
# RETRIEVER AGENT
# -------------------


def retriever_agent(
    state: WorkflowState,
) -> dict:
    """
    Retrieves relevant knowledge from ChromaDB.
    """

    print("Retriever Agent")

    results = collection.query(
        query_texts=[
            state["question"],
        ],
        n_results=1,
    )

    retrieved_knowledge = results["documents"][0][0]

    return {"retrieved_knowledge": retrieved_knowledge}


# -------------------
# TOOL AGENT
# -------------------


def tool_agent(
    state: WorkflowState,
) -> dict:
    """
    Executes a tool when the question
    requires tool support.
    """

    print("Tool Agent")

    question = state["question"].lower()

    if "%" in question or "percent" in question:
        return {"tool_result": calculator_tool()}

    return {"tool_result": "No tool needed."}


# -------------------
# ANSWER AGENT
# -------------------


def answer_agent(
    state: WorkflowState,
) -> dict:
    """
    Generates or revises an answer using:
    - retrieved knowledge
    - tool result

    If the previous answer was rejected,
    the agent attempts one revision.
    """

    print("Answer Agent")

    if state["review"] == "NEEDS_REVISION":
        prompt = f"""
Question:
{state["question"]}

Retrieved Knowledge:
{state["retrieved_knowledge"]}

Tool Result:
{state["tool_result"]}

Previous Answer:
{state["answer"]}

The previous answer added unsupported information.

Revise the answer using ONLY the retrieved knowledge and tool result.
Return exactly 3 short bullet points.
Do not add formulas unless they are explicitly in the retrieved knowledge or tool result.

Answer:
"""
    else:
        prompt = f"""
Question:
{state["question"]}

Retrieved Knowledge:
{state["retrieved_knowledge"]}

Tool Result:
{state["tool_result"]}

Instructions:
- Use ONLY the retrieved knowledge and tool result.
- Return exactly 3 short bullet points.
- Do not add unsupported facts.

Answer:
"""

    response = llm.invoke(prompt)

    return {"answer": response.content}


# -------------------
# ANSWER REVIEW AGENT
# -------------------


def answer_review_agent(
    state: WorkflowState,
) -> dict:
    """
    Reviews whether the answer is supported
    by the retrieved knowledge and tool result.
    """

    print("Answer Review Agent")

    response = llm.invoke(f"""
Question:
{state["question"]}

Retrieved Knowledge:
{state["retrieved_knowledge"]}

Tool Result:
{state["tool_result"]}

Answer:
{state["answer"]}

Review the answer.

Return ONLY one word:
APPROVED
or
NEEDS_REVISION

Return NEEDS_REVISION if the answer adds unsupported information.
Return APPROVED only if the answer is grounded in the retrieved knowledge and tool result.
""")

    review = response.content.strip().upper()

    if review not in [
        "APPROVED",
        "NEEDS_REVISION",
    ]:
        review = "NEEDS_REVISION"

    return {"review": review}


# -------------------
# ROUTING FUNCTION
# -------------------


def route_after_review(
    state: WorkflowState,
) -> Literal["increment_revision", "final_decision_agent"]:
    """
    Routes workflow after answer review.

    APPROVED
        -> final_decision_agent

    NEEDS_REVISION and revision_count < 1
        -> increment_revision

    NEEDS_REVISION and revision_count >= 1
        -> final_decision_agent
    """

    if state["review"] == "APPROVED":
        return "final_decision_agent"

    if state["revision_count"] >= 1:
        return "final_decision_agent"

    return "increment_revision"


# -------------------
# REVISION COUNTER
# -------------------


def increment_revision(
    state: WorkflowState,
) -> dict:
    """
    Increments revision count before sending
    the answer back for revision.
    """

    print("Increment Revision Count")

    return {"revision_count": state["revision_count"] + 1}


# -------------------
# FINAL DECISION AGENT
# -------------------


def final_decision_agent(
    state: WorkflowState,
) -> dict:
    """
    Makes the final workflow decision before
    human approval.
    """

    print("Final Decision Agent")

    if state["review"] == "APPROVED":
        return {"status": "approved"}

    return {"status": "needs_manual_review"}


# -------------------
# HUMAN APPROVAL
# -------------------


def human_approval(
    state: WorkflowState,
) -> dict:
    """
    Human approval step.

    The human reviewer approves or rejects
    the final workflow output.
    """

    print("\nHuman Approval Required")
    print("=" * 60)

    print("\nStatus:")
    print(state["status"])

    print("\nAnswer:")
    print(state["answer"])

    print("\nReview:")
    print(state["review"])

    decision = input("\nEnter decision (APPROVE / REJECT): ").strip().upper()

    if decision not in [
        "APPROVE",
        "REJECT",
    ]:
        decision = "REJECT"

    return {"human_decision": decision}


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
    "retriever_agent",
    retriever_agent,
)

graph.add_node(
    "tool_agent",
    tool_agent,
)

graph.add_node(
    "answer_agent",
    answer_agent,
)

graph.add_node(
    "answer_review_agent",
    answer_review_agent,
)

graph.add_node(
    "increment_revision",
    increment_revision,
)

graph.add_node(
    "final_decision_agent",
    final_decision_agent,
)

graph.add_node(
    "human_approval",
    human_approval,
)


# -------------------
# GRAPH EDGES
# -------------------

graph.add_edge(
    START,
    "retriever_agent",
)

graph.add_edge(
    "retriever_agent",
    "tool_agent",
)

graph.add_edge(
    "tool_agent",
    "answer_agent",
)

graph.add_edge(
    "answer_agent",
    "answer_review_agent",
)

graph.add_conditional_edges(
    "answer_review_agent",
    route_after_review,
    {
        "increment_revision": "increment_revision",
        "final_decision_agent": "final_decision_agent",
    },
)

graph.add_edge(
    "increment_revision",
    "answer_agent",
)

graph.add_edge(
    "final_decision_agent",
    "human_approval",
)

graph.add_edge(
    "human_approval",
    END,
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
            "question": "How do percentages work?",
            "retrieved_knowledge": "",
            "tool_result": "",
            "answer": "",
            "review": "",
            "revision_count": 0,
            "status": "not_started",
            "human_decision": "",
        }
    ),
)


# -------------------
# DISPLAY RESULT
# -------------------

display_result(result)
