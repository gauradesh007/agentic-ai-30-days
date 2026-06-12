import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# -------------------
# MODEL CLIENT
# -------------------

model_client = OpenAIChatCompletionClient(
    model="llama3.2:1b",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model_info={
        "vision": False,
        "function_calling": False,
        "json_output": False,
        "structured_output": False,
        "family": "llama",
    },
)


# -------------------
# AGENTS
# -------------------

research_agent = AssistantAgent(
    name="research_agent",
    model_client=model_client,
    system_message=(
        "You are a research agent.\n"
        "ONLY provide factual research.\n"
        "DO NOT rewrite for beginners.\n"
        "DO NOT review outputs.\n"
        "DO NOT provide bullet points.\n"
        "Your responsibility is research only."
    ),
)

writer_agent = AssistantAgent(
    name="writer_agent",
    model_client=model_client,
    system_message=(
        "You are a technical writer.\n"
        "ONLY rewrite research into a beginner-friendly explanation.\n"
        "DO NOT perform research.\n"
        "DO NOT review outputs.\n"
        "Your responsibility is writing only."
    ),
)

reviewer_agent = AssistantAgent(
    name="reviewer_agent",
    model_client=model_client,
    system_message=(
        "You are a reviewer.\n"
        "ONLY review the writer's output.\n"
        "DO NOT perform research.\n"
        "DO NOT rewrite the explanation.\n"
        "End your review with APPROVED if acceptable."
    ),
)


# -------------------
# TERMINATION CONDITION
# -------------------

termination = MaxMessageTermination(max_messages=6)


# -------------------
# TEAM CHAT
# -------------------

team = RoundRobinGroupChat(
    participants=[
        research_agent,
        writer_agent,
        reviewer_agent,
    ],
    termination_condition=termination,
)


# -------------------
# EXECUTION
# -------------------


async def main() -> None:
    """
    Runs a multi-agent AutoGen conversation
    with a research agent, writer agent,
    and reviewer agent.
    """

    stream = team.run_stream(
        task=(
            "Explain what an AI agent is.\n"
            "Research agent should provide research only.\n"
            "Writer agent should rewrite for beginners.\n"
            "Reviewer agent should review the writer's explanation.\n"
            "Each agent must stay within its assigned role."
        )
    )

    await Console(stream)

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
