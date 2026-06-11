from crewai import Agent
from crewai import Crew
from crewai import LLM
from crewai import Task

# -------------------
# LOCAL LLM
# -------------------

llm = LLM(
    model="ollama/llama3.2:1b",
    base_url="http://localhost:11434",
)


# -------------------
# AGENTS
# -------------------

researcher = Agent(
    role="Research Specialist",
    goal="Research AI concepts clearly and accurately.",
    backstory=(
        "You are a research specialist who explains technical AI concepts "
        "in simple and accurate language."
    ),
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Technical Writer",
    goal="Turn research into a clear beginner-friendly explanation.",
    backstory=(
        "You are a technical writer who converts research notes into "
        "simple, structured explanations."
    ),
    llm=llm,
    verbose=True,
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Review the explanation for clarity, accuracy, and completeness.",
    backstory=(
        "You are a quality reviewer who checks whether explanations are "
        "clear, accurate, and useful for beginners."
    ),
    llm=llm,
    verbose=True,
)


validator = Agent(
    role="Output Validator",
    goal="Validate whether the final explanation follows the required format.",
    backstory=(
        "You are a strict output validator. "
        "You check whether the final response follows the requested format exactly."
    ),
    llm=llm,
    verbose=True,
)


# -------------------
# TASKS
# -------------------

research_task = Task(
    description=(
        "Research what an AI agent is. " "Explain the key idea in simple terms."
    ),
    expected_output=("A short research summary explaining what an AI agent is."),
    agent=researcher,
)

writing_task = Task(
    description=(
        "Using the research summary, write a beginner-friendly explanation "
        "of what an AI agent is in 3 short bullet points."
    ),
    expected_output=("Three short bullet points explaining what an AI agent is."),
    agent=writer,
    context=[
        research_task,
    ],
)

review_task = Task(
    description=(
        "Review the writer's explanation. "
        "Confirm whether it is clear, accurate, and beginner-friendly. "
        "If needed, improve it."
    ),
    expected_output=("A final reviewed explanation of what an AI agent is."),
    agent=reviewer,
    context=[
        writing_task,
    ],
)

validation_task = Task(
    description=(
        "Validate the reviewed explanation. "
        "Check whether it contains exactly 3 short bullet points. "
        "Return PASS if it follows the requirement. "
        "Return FAIL if it does not. "
        "If it fails, explain what went wrong."
    ),
    expected_output=("PASS or FAIL with a short explanation."),
    agent=validator,
    context=[
        review_task,
    ],
)

# -------------------
# CREW
# -------------------

crew = Crew(
    agents=[
        researcher,
        writer,
        reviewer,
        validator,
    ],
    tasks=[
        research_task,
        writing_task,
        review_task,
        validation_task,
    ],
    verbose=True,
)


# -------------------
# EXECUTION
# -------------------

result = crew.kickoff()

print("\nFINAL REVIEWED RESULT:")
print(result)
