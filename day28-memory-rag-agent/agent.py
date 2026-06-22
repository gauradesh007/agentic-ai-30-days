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
# CHROMADB MEMORY
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
    Shared workflow state.

    This state stores:
    - user question
    - retrieved knowledge from ChromaDB
    - generated answer
    - review decision
    - revision count
    - final workflow status
    """

    question: str
    retrieved_knowledge: str
    answer: str
    review: str
    revision_count: int
    status: str


# -------------------
# RETRIEVER AGENT
# -------------------


def retriever_agent(
    state: WorkflowState,
) -> dict:
    """
    Retrieves the most relevant knowledge
    from ChromaDB based on the question.
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
# ANSWER AGENT
# -------------------


def answer_agent(
    state: WorkflowState,
) -> dict:
    """
    Generates an answer using retrieved knowledge.

    If the previous answer was rejected,
    the agent revises the answer using only
    the retrieved knowledge.
    """

    print("Answer Agent")

    if state["review"] == "NEEDS_REVISION":
        prompt = f"""
Question:
{state["question"]}

Retrieved Knowledge:
{state["retrieved_knowledge"]}

Previous Answer:
{state["answer"]}

The previous answer added unsupported information.

Revise the answer using ONLY the retrieved knowledge.
Return exactly 3 short bullet points.
Do not add formulas unless they are explicitly in the retrieved knowledge.

Answer:
"""
    else:
        prompt = f"""
Question:
{state["question"]}

Retrieved Knowledge:
{state["retrieved_knowledge"]}

Instructions:
- Use ONLY the retrieved knowledge.
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
    Reviews whether the generated answer
    follows the retrieved knowledge.
    """

    print("Answer Review Agent")

    response = llm.invoke(f"""
Question:
{state["question"]}

Retrieved Knowledge:
{state["retrieved_knowledge"]}

Answer:
{state["answer"]}

Review the answer.

Return ONLY one word:
APPROVED
or
NEEDS_REVISION

Return NEEDS_REVISION if the answer adds information
that is not supported by the retrieved knowledge.
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
) -> Literal["increment_revision", "final_rag_decision"]:
    """
    Routes the workflow after answer review.

    APPROVED
        -> final_rag_decision

    NEEDS_REVISION and revision_count < 1
        -> increment_revision

    NEEDS_REVISION and revision_count >= 1
        -> final_rag_decision
    """

    if state["review"] == "APPROVED":
        return "final_rag_decision"

    if state["revision_count"] >= 1:
        return "final_rag_decision"

    return "increment_revision"


# -------------------
# REVISION COUNTER
# -------------------


def increment_revision(
    state: WorkflowState,
) -> dict:
    """
    Increments the answer revision count
    before sending the answer back for revision.
    """

    print("Increment Revision Count")

    return {"revision_count": state["revision_count"] + 1}


# -------------------
# FINAL DECISION NODE
# -------------------


def final_rag_decision(
    state: WorkflowState,
) -> dict:
    """
    Makes the final RAG workflow decision.

    The workflow ends as approved if the
    answer passed review.

    Otherwise, it ends with a RAG error status
    and requires manual correction.
    """

    print("Final RAG Decision")

    if state["review"] == "APPROVED":
        return {"status": "approved"}

    return {
        "status": "completed_with_rag_errors",
        "review": (
            state["review"] + "\n\nFinal Decision: RAG answer still needs review. "
            "Manual correction required."
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
    "retriever_agent",
    retriever_agent,
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
    "final_rag_decision",
    final_rag_decision,
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
        "final_rag_decision": "final_rag_decision",
    },
)

graph.add_edge(
    "increment_revision",
    "answer_agent",
)

graph.add_edge(
    "final_rag_decision",
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
            "answer": "",
            "review": "",
            "revision_count": 0,
            "status": "not_started",
        }
    ),
)


# -------------------
# DISPLAY RESULT
# -------------------

display_result(result)
