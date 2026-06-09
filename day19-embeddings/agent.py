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
    Saves memory to memory.json.
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
# SIMPLE EMBEDDING
# -------------------


def create_embedding(text: str) -> list:
    """
    Creates a very simple embedding.

    Each word becomes one dimension.

    The value of each dimension is the
    number of characters in the word.

    NOTE:
    This is NOT a real embedding model.
    It is only used to demonstrate
    embedding architecture.
    """

    words = text.lower().split()

    embedding = []

    for word in words:
        embedding.append(len(word))

    return embedding


# -------------------
# VECTOR DISTANCE
# -------------------


def vector_similarity(
    vector1: list,
    vector2: list,
) -> int:
    """
    Calculates vector distance.

    Lower score = closer vectors.

    NOTE:
    This is NOT cosine similarity.
    It is a simplified distance calculation
    used for learning purposes.
    """

    distance = 0

    shortest_length = min(
        len(vector1),
        len(vector2),
    )

    for i in range(shortest_length):
        distance += abs(vector1[i] - vector2[i])

    return distance


# -------------------
# EMBEDDING RETRIEVAL
# -------------------


def retrieve_by_embedding(
    memory: list,
    query: str,
) -> dict:
    """
    Retrieves the memory item with the
    lowest vector distance.

    Steps:
    - embed query
    - embed each memory item
    - calculate distance
    - return closest memory
    """

    query_embedding = create_embedding(query)

    best_memory = None
    lowest_distance = float("inf")

    for item in memory:

        memory_embedding = create_embedding(item["content"])

        distance = vector_similarity(
            query_embedding,
            memory_embedding,
        )

        if distance < lowest_distance:
            lowest_distance = distance
            best_memory = item

    return {
        "memory": best_memory,
        "distance": lowest_distance,
    }


# -------------------
# LOAD MEMORY
# -------------------

memory = load_memory()


# -------------------
# STORE SAMPLE MEMORIES
# -------------------

remember(
    memory,
    {
        "topic": "math",
        "content": ("Percentage calculations " "use decimal multiplication."),
    },
)

remember(
    memory,
    {
        "topic": "date",
        "content": ("Current date returns " "the real system date."),
    },
)

remember(
    memory,
    {
        "topic": "text",
        "content": ("Text length counts " "characters in a string."),
    },
)


# -------------------
# DISPLAY MEMORY EMBEDDINGS
# -------------------

print("\nEMBEDDINGS:")

for item in memory:

    embedding = create_embedding(item["content"])

    print(
        item["topic"],
        "->",
        embedding,
    )


# -------------------
# QUERY EMBEDDING
# -------------------

query = "How do I calculate percentages?"

query_embedding = create_embedding(query)

print("\nQUERY EMBEDDING:")
print(query_embedding)


# -------------------
# VECTOR DISTANCE TESTS
# -------------------

print("\nVECTOR DISTANCES:")

for item in memory:

    memory_embedding = create_embedding(item["content"])

    distance = vector_similarity(
        query_embedding,
        memory_embedding,
    )

    print(
        item["topic"],
        "-> distance:",
        distance,
    )


# -------------------
# EMBEDDING RETRIEVAL TEST
# -------------------

print("\nEMBEDDING RETRIEVAL:")

embedding_result = retrieve_by_embedding(
    memory,
    query,
)

print(
    "Distance:",
    embedding_result["distance"],
)

print(
    "Memory:",
    embedding_result["memory"],
)
