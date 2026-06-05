import json

# -------------------
# MEMORY LOADER
# -------------------


def load_memory() -> list:
    """
    Loads persistent memory from disk.

    If memory.json does not exist or cannot be loaded,
    an empty memory list is returned.
    """

    try:
        with open(
            "memory.json",
            "r",
        ) as file:
            return json.load(file)

    except Exception:
        return []


# -------------------
# MEMORY SAVER
# -------------------


def save_memory(memory: list) -> None:
    """
    Saves memory to disk.

    The memory list is written to memory.json.
    """

    with open(
        "memory.json",
        "w",
    ) as file:
        json.dump(
            memory,
            file,
            indent=4,
        )


# -------------------
# MEMORY WRITER
# -------------------


def remember(
    memory: list,
    item: dict,
) -> None:
    """
    Stores a new memory item.

    Duplicate memories are ignored.
    """

    if item not in memory:
        memory.append(item)

        save_memory(memory)

        print("Memory stored.")

    else:
        print("Memory already exists.")


# -------------------
# MEMORY RETRIEVAL
# -------------------


def retrieve_memory(
    memory: list,
    topic: str,
) -> list:
    """
    Retrieves memory entries matching a topic.

    Example:
    topic = "agentic_ai"
    """

    results = []

    for item in memory:
        if item["topic"] == topic:
            results.append(item)

    return results


# -------------------
# MEMORY KEYWORD SEARCH
# -------------------


def search_memory(
    memory: list,
    keyword: str,
) -> list:
    """
    Searches memory by keyword.

    The keyword is matched against:
    - topic
    - content

    This is more flexible than exact topic retrieval.
    """

    keyword = keyword.lower()
    results = []

    for item in memory:
        topic = item["topic"].lower()
        content = item["content"].lower()

        if keyword in topic or keyword in content:
            results.append(item)

    return results


# -------------------
# LOAD MEMORY
# -------------------

memory = load_memory()


# -------------------
# STORE MEMORY
# -------------------

remember(
    memory,
    {
        "topic": "agentic_ai",
        "content": "Persistent memory survives program restarts.",
    },
)


# -------------------
# DISPLAY MEMORY
# -------------------

print("\nLOADED MEMORY:")
print(memory)


# -------------------
# TOPIC RETRIEVAL
# -------------------

print("\nRETRIEVED MEMORY:")

retrieved_results = retrieve_memory(
    memory,
    "agentic_ai",
)

for item in retrieved_results:
    print(item)


# -------------------
# KEYWORD SEARCH
# -------------------

print("\nKEYWORD SEARCH RESULTS:")

search_results = search_memory(
    memory,
    "persistent",
)

for item in search_results:
    print(item)
