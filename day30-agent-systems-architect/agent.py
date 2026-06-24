import chromadb

from typing import Literal
from typing import TypedDict
from typing import cast

from langchain_ollama import ChatOllama
from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

# =====================================================
# DAY 30 CAPSTONE
# BOOMI INTEGRATION ARCHITECT AGENT
#
# Features:
# - Planning
# - Retrieval with ChromaDB
# - Tool Calling
# - Architecture Generation
# - Architecture Review
# - Revision Loop
# - Final Polish
# - Human Approval
# =====================================================


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

collection = client.get_or_create_collection(name="integration_architecture_knowledge")

collection.add(
    documents=[
        "REST API integrations are suitable for synchronous request-response communication.",
        "Event-driven integrations are suitable for asynchronous processing.",
        "Retry logic should be used for transient failures.",
        "API-led architecture improves reusability and scalability.",
        "Field mapping should be validated before loading data into SAP.",
        "Salesforce is commonly used as a source system and SAP as a target system.",
        "Boomi Salesforce Connector supports real-time and batch integrations.",
        "Boomi SAP integrations commonly use REST APIs, OData services, IDocs, or BAPIs.",
        "Error handling should use try/catch and process reporting.",
        "Monitoring should use AtomSphere process reporting, execution dashboards, and Boomi process logging.",
        "Data validation should occur before transformation and SAP loading.",
        "API-led architecture promotes reusable integrations.",
    ],
    ids=[
        "rest",
        "event",
        "retry",
        "api_led",
        "mapping",
        "salesforce_sap",
        "sf_connector",
        "sap_connector",
        "error_handling",
        "monitoring",
        "validation",
        "api_led_architecture",
    ],
)


# -------------------
# WORKFLOW STATE
# -------------------


class WorkflowState(TypedDict):
    """
    Shared workflow state for the capstone agent.

    Stores:
    - integration request
    - implementation plan
    - retrieved architecture knowledge
    - tool result
    - generated architecture report
    - architecture review result
    - revision count
    - final workflow status
    - human approval decision
    """

    request: str
    plan: str
    retrieved_knowledge: str
    tool_result: str
    architecture: str
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

    Included to demonstrate the tool layer.
    """

    result = (25 / 100) * 400

    return f"Tool result: 25% of 400 is {result}."


# -------------------
# PLANNER AGENT
# -------------------


def planner_agent(
    state: WorkflowState,
) -> dict:
    """
    Creates a short implementation plan
    for the integration request.
    """

    print("Planner Agent")

    response = llm.invoke(f"""
You are an Integration Architect.

Integration Request:
{state["request"]}

Create a short implementation plan.

Return exactly 4 bullet points.
""")

    return {"plan": response.content}


# -------------------
# RETRIEVER AGENT
# -------------------


def retriever_agent(
    state: WorkflowState,
) -> dict:
    """
    Retrieves relevant architecture knowledge
    from ChromaDB.
    """

    print("Retriever Agent")

    results = collection.query(
        query_texts=[
            state["request"],
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
    Executes supporting tools for
    integration architecture generation.
    """

    print("Tool Agent")

    request = state["request"].lower()

    if "%" in request or "percent" in request:
        return {"tool_result": calculator_tool()}

    return {"tool_result": "No tool needed."}


# -------------------
# ARCHITECTURE AGENT
# -------------------


def architecture_agent(
    state: WorkflowState,
) -> dict:
    """
    Generates or revises a Boomi-oriented
    integration architecture report.
    """

    print("Architecture Agent")

    if state["review"] == "NEEDS_REVISION":
        prompt = f"""
You are a Senior Boomi Integration Architect.

Integration Request:
{state["request"]}

Implementation Plan:
{state["plan"]}

Retrieved Knowledge:
{state["retrieved_knowledge"]}

Tool Result:
{state["tool_result"]}

Previous Architecture:
{state["architecture"]}

The previous architecture did not fully satisfy the review criteria.

Revise the Salesforce to SAP integration architecture report.

Strict rules:
- Salesforce must be the source system.
- SAP must be the target system.
- Boomi must be the integration layer.
- Do not reverse the data direction.
- Do not mention SAP as the source.
- Do not mention Salesforce as the target.
- Keep the report concise and practical.

Return exactly these sections:

1. Requirement Summary
2. Recommended Pattern
3. Boomi Process Flow
4. Connector Strategy
5. Mapping Strategy
6. Error Handling
7. Monitoring
8. Security Considerations
9. Risks and Assumptions
10. Final Recommendation
"""
    else:
        prompt = f"""
You are a Senior Boomi Integration Architect.

Integration Request:
{state["request"]}

Implementation Plan:
{state["plan"]}

Retrieved Knowledge:
{state["retrieved_knowledge"]}

Tool Result:
{state["tool_result"]}

Create a Salesforce to SAP integration architecture report.

Strict rules:
- Salesforce must be the source system.
- SAP must be the target system.
- Boomi must be the integration layer.
- Do not reverse the data direction.
- Do not mention SAP as the source.
- Do not mention Salesforce as the target.
- Keep the report concise and practical.

Return exactly these sections:

1. Requirement Summary
2. Recommended Pattern
3. Boomi Process Flow
4. Connector Strategy
5. Mapping Strategy
6. Error Handling
7. Monitoring
8. Security Considerations
9. Risks and Assumptions
10. Final Recommendation
"""

    response = llm.invoke(prompt)

    return {"architecture": response.content}


# -------------------
# ARCHITECTURE REVIEW AGENT
# -------------------


def architecture_review_agent(
    state: WorkflowState,
) -> dict:
    """
    Reviews whether the architecture report
    satisfies the required integration criteria.
    """

    print("Architecture Review Agent")

    response = llm.invoke(f"""
You are a strict architecture reviewer.

Integration Request:
{state["request"]}

Architecture:
{state["architecture"]}

Review the architecture report.

Return ONLY one word:
APPROVED
or
NEEDS_REVISION

Return APPROVED only if:
- Salesforce is clearly the source system.
- SAP is clearly the target system.
- Boomi is clearly the integration layer.
- The report includes Boomi Process Flow.
- The report includes Error Handling.
- The report includes Monitoring.
- The report includes Security Considerations.

Return NEEDS_REVISION if any requirement is missing or the data direction is reversed.
""")

    review = response.content.strip().upper()

    if review not in [
        "APPROVED",
        "NEEDS_REVISION",
    ]:
        review = "NEEDS_REVISION"

    return {"review": review}


# -------------------
# FINAL POLISH AGENT
# -------------------


def final_polish_agent(
    state: WorkflowState,
) -> dict:
    """
    Polishes the architecture report into a
    final portfolio-ready format.
    """

    print("Final Polish Agent")

    response = llm.invoke(f"""
You are a Senior Boomi Integration Architect.

Rewrite the architecture report into a final clean version.

Integration Request:
{state["request"]}

Current Architecture:
{state["architecture"]}

Strict requirements:
- Clearly state: Salesforce is the source system.
- Clearly state: SAP is the target system.
- Clearly state: Boomi is the integration layer.
- Do not reverse the data direction.
- Keep the design practical and enterprise-oriented.

Return exactly these sections:

1. Requirement Summary
2. Recommended Integration Pattern
3. Source System
4. Target System
5. Boomi Process Flow
6. Connector Strategy
7. Mapping Strategy
8. Error Handling Strategy
9. Monitoring and Logging
10. Security Considerations
11. Risks and Assumptions
12. Final Recommendation
""")

    return {"architecture": response.content}


# -------------------
# ROUTING FUNCTION
# -------------------


def route_after_review(
    state: WorkflowState,
) -> Literal["increment_revision", "final_polish_agent"]:
    """
    Routes workflow after architecture review.

    APPROVED
        -> final_polish_agent

    NEEDS_REVISION and revision_count < 1
        -> increment_revision

    NEEDS_REVISION and revision_count >= 1
        -> final_polish_agent
    """

    if state["review"] == "APPROVED":
        return "final_polish_agent"

    if state["revision_count"] >= 1:
        return "final_polish_agent"

    return "increment_revision"


# -------------------
# REVISION COUNTER
# -------------------


def increment_revision(
    state: WorkflowState,
) -> dict:
    """
    Increments revision count before sending
    the architecture report back for revision.
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
    the final architecture report.
    """

    print("\nHuman Approval Required")
    print("=" * 60)

    print("\nStatus:")
    print(state["status"])

    print("\nArchitecture:")
    print(state["architecture"])

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

graph.add_node("planner_agent", planner_agent)
graph.add_node("retriever_agent", retriever_agent)
graph.add_node("tool_agent", tool_agent)
graph.add_node("architecture_agent", architecture_agent)
graph.add_node("architecture_review_agent", architecture_review_agent)
graph.add_node("increment_revision", increment_revision)
graph.add_node("final_polish_agent", final_polish_agent)
graph.add_node("final_decision_agent", final_decision_agent)
graph.add_node("human_approval", human_approval)


# -------------------
# GRAPH EDGES
# -------------------

graph.add_edge(START, "planner_agent")
graph.add_edge("planner_agent", "retriever_agent")
graph.add_edge("retriever_agent", "tool_agent")
graph.add_edge("tool_agent", "architecture_agent")
graph.add_edge("architecture_agent", "architecture_review_agent")

graph.add_conditional_edges(
    "architecture_review_agent",
    route_after_review,
    {
        "increment_revision": "increment_revision",
        "final_polish_agent": "final_polish_agent",
    },
)

graph.add_edge("increment_revision", "architecture_agent")
graph.add_edge("final_polish_agent", "final_decision_agent")
graph.add_edge("final_decision_agent", "human_approval")
graph.add_edge("human_approval", END)


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
            "request": "Design a Salesforce to SAP integration using Boomi.",
            "plan": "",
            "architecture": "",
            "retrieved_knowledge": "",
            "tool_result": "",
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
