import json

# -------------------
# MEMORY LOADER
# -------------------


def load_memory() -> list:
    """
    Loads persistent memory from memory.json.

    If the file does not exist or cannot be read,
    an empty memory list is returned.
    """

    try:
        with open("memory.json", "r") as file:
            return json.load(file)

    except Exception:
        return []


# -------------------
# MEMORY SAVER
# -------------------


def save_memory(memory: list) -> None:
    """
    Saves memory to memory.json.
    """

    with open("memory.json", "w") as file:
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
# MEMORY RANKING
# -------------------


def rank_memories(
    memory: list,
    query: str,
) -> list:
    """
    Ranks memory items using simple keyword matching.

    Scoring rule:
    - split query into words
    - match words against topic + content
    - add 1 point for every match
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
    Returns the highest-ranked keyword memory match.

    If no result has a positive score,
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
    Returns the best keyword match only if
    it meets the minimum threshold.
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
# SEMANTIC GROUPS
# -------------------

SEMANTIC_GROUPS = {
    "math": [
        "percent",
        "percentage",
        "calculate",
        "calculation",
        "multiply",
        "decimal",
    ],
    "date": [
        "today",
        "date",
        "day",
        "current",
        "system",
    ],
    "text": [
        "text",
        "string",
        "character",
        "characters",
        "length",
    ],
}


# -------------------
# SEMANTIC EXPANSION
# -------------------


def expand_query_semantically(query: str) -> list:
    """
    Expands a query into semantic meaning groups.

    Example:
    "How do I find 15 percent of 5000?"
    becomes:
    ["math"]
    """

    query_words = query.lower().split()
    matched_groups = []

    for group_name, group_words in SEMANTIC_GROUPS.items():
        for word in query_words:
            if word in group_words:
                matched_groups.append(group_name)
                break

    return matched_groups


# -------------------
# SEMANTIC MEMORY RANKING
# -------------------


def rank_memories_semantically(
    memory: list,
    query: str,
) -> list:
    """
    Ranks memories using semantic groups.

    Instead of only matching exact query words,
    this function maps the query to a meaning group
    and scores memories related to that group.
    """

    matched_groups = expand_query_semantically(query)
    ranked_results = []

    for item in memory:
        score = 0

        topic = item["topic"].lower()
        content = item["content"].lower()

        for group in matched_groups:
            group_words = SEMANTIC_GROUPS[group]

            if topic == group:
                score += 2

            for word in group_words:
                if word in content:
                    score += 1

        ranked_results.append(
            {
                "memory": item,
                "score": score,
                "matched_groups": matched_groups,
            }
        )

    ranked_results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return ranked_results


# -------------------
# BEST SEMANTIC MEMORY MATCH
# -------------------


def get_best_semantic_match(
    memory: list,
    query: str,
) -> dict | None:
    """
    Returns the highest-ranked semantic memory match.

    If no semantic result has a positive score,
    returns None.
    """

    ranked_results = rank_memories_semantically(
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
# SEMANTIC THRESHOLD MATCH
# -------------------


def get_semantic_match_with_threshold(
    memory: list,
    query: str,
    threshold: int,
) -> dict | None:
    """
    Returns the best semantic match only if
    it meets the minimum threshold.
    """

    best_match = get_best_semantic_match(
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
# KEYWORD RANKING TEST
# -------------------

print("\nRANKED MEMORIES:")

ranked_results = rank_memories(
    memory,
    "percentage calculation",
)

for item in ranked_results:
    print(f"Score: {item['score']} | " f"{item['memory']}")


# -------------------
# BEST KEYWORD MATCH TEST
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
# KEYWORD THRESHOLD TEST
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
# STRICT KEYWORD THRESHOLD TEST
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


# -------------------
# SEMANTIC GROUP TEST
# -------------------

semantic_query = "How do I find 15 percent of 5000?"

print("\nSEMANTIC GROUPS MATCHED:")

matched_groups = expand_query_semantically(
    semantic_query,
)

print(matched_groups)


# -------------------
# SEMANTIC RANKING TEST
# -------------------

print("\nSEMANTIC RANKED MEMORIES:")

semantic_ranked = rank_memories_semantically(
    memory,
    semantic_query,
)

for item in semantic_ranked:
    print(
        f"Score: {item['score']} | "
        f"Groups: {item['matched_groups']} | "
        f"{item['memory']}"
    )


# -------------------
# BEST SEMANTIC MATCH TEST
# -------------------

print("\nBEST SEMANTIC MATCH:")

best_semantic_match = get_best_semantic_match(
    memory,
    semantic_query,
)

if best_semantic_match:
    print(
        f"Score: {best_semantic_match['score']} | "
        f"Groups: {best_semantic_match['matched_groups']} | "
        f"{best_semantic_match['memory']}"
    )
else:
    print("No relevant semantic memory found.")


# -------------------
# SEMANTIC THRESHOLD TEST
# -------------------

print("\nSEMANTIC THRESHOLD MATCH TEST:")

semantic_threshold_match = get_semantic_match_with_threshold(
    memory,
    semantic_query,
    4,
)

if semantic_threshold_match:
    print(
        f"Accepted | "
        f"Score: {semantic_threshold_match['score']} | "
        f"Groups: {semantic_threshold_match['matched_groups']} | "
        f"{semantic_threshold_match['memory']}"
    )
else:
    print("Rejected: semantic score below threshold.")


# -------------------
# STRICT SEMANTIC THRESHOLD TEST
# -------------------

print("\nSTRICT SEMANTIC THRESHOLD TEST:")

strict_semantic_match = get_semantic_match_with_threshold(
    memory,
    semantic_query,
    10,
)

if strict_semantic_match:
    print(
        f"Accepted | "
        f"Score: {strict_semantic_match['score']} | "
        f"Groups: {strict_semantic_match['matched_groups']} | "
        f"{strict_semantic_match['memory']}"
    )
else:
    print("Rejected: semantic score below threshold.")
