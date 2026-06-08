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

    This is exact topic-based retrieval.
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
# MEMORY RANKING
# -------------------


def rank_memories(
    memory: list,
    query: str,
) -> list:
    """
    Assigns a simple relevance score to each memory item.

    Scoring rule:
    - split the query into words
    - check each word against topic + content
    - add 1 point for each matched word

    More keyword matches = higher score.
    """

    query_words = query.lower().split()
    ranked_results = []

    for item in memory:
        score = 0

        searchable_text = (item["topic"] + " " + item["content"]).lower()

        for word in query_words:
            if word in searchable_text:
                score += 1

        ranked_results.append(
            {
                "memory": item,
                "score": score,
            }
        )

    ranked_results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return ranked_results


# -------------------
# BEST MEMORY MATCH
# -------------------


def get_best_memory_match(
    memory: list,
    query: str,
) -> dict | None:
    """
    Returns the highest-ranked memory item.

    If no memory has a positive score,
    returns None.
    """

    ranked_results = rank_memories(
        memory,
        query,
    )

    if not ranked_results:
        return None

    best_match = ranked_results[0]

    if best_match["score"] == 0:
        return None

    return best_match


# -------------------
# THRESHOLD MEMORY MATCH
# -------------------


def get_memory_match_with_threshold(
    memory: list,
    query: str,
    threshold: int,
) -> dict | None:
    """
    Returns the best memory match only if
    the score meets the minimum threshold.

    This prevents weak matches from being accepted.
    """

    best_match = get_best_memory_match(
        memory,
        query,
    )

    if best_match is None:
        return None

    if best_match["score"] < threshold:
        return None

    return best_match


# -------------------
# LOAD MEMORY
# -------------------

memory = load_memory()


# -------------------
# STORE SAMPLE MEMORY
# -------------------

remember(
    memory,
    {
        "topic": "math",
        "content": "Percentage calculations use decimal multiplication.",
    },
)

remember(
    memory,
    {
        "topic": "date",
        "content": "Current date returns the real system date.",
    },
)

remember(
    memory,
    {
        "topic": "text",
        "content": "Text length counts characters in a string.",
    },
)


# -------------------
# RANK ALL MEMORIES
# -------------------

print("\nRANKED MEMORIES:")

ranked_results = rank_memories(
    memory,
    "percentage calculation",
)

for item in ranked_results:
    print(f"Score: {item['score']} | " f"{item['memory']}")


# -------------------
# BEST MATCH TEST
# -------------------

print("\nBEST MEMORY MATCH:")

best_match = get_best_memory_match(
    memory,
    "percentage calculation",
)

if best_match:
    print(f"Score: {best_match['score']} | " f"{best_match['memory']}")
else:
    print("No relevant memory found.")


# -------------------
# NO MATCH TEST
# -------------------

print("\nNO MATCH TEST:")

no_match = get_best_memory_match(
    memory,
    "weather forecast",
)

if no_match:
    print(f"Score: {no_match['score']} | " f"{no_match['memory']}")
else:
    print("No relevant memory found.")


# -------------------
# THRESHOLD MATCH TEST
# -------------------

print("\nTHRESHOLD MATCH TEST:")

threshold_match = get_memory_match_with_threshold(
    memory,
    "percentage calculation",
    2,
)

if threshold_match:
    print(
        f"Accepted | "
        f"Score: {threshold_match['score']} | "
        f"{threshold_match['memory']}"
    )
else:
    print("Rejected: score below threshold.")


# -------------------
# STRICT THRESHOLD TEST
# -------------------

print("\nSTRICT THRESHOLD TEST:")

strict_match = get_memory_match_with_threshold(
    memory,
    "percentage calculation",
    3,
)

if strict_match:
    print(
        f"Accepted | " f"Score: {strict_match['score']} | " f"{strict_match['memory']}"
    )
else:
    print("Rejected: score below threshold.")
