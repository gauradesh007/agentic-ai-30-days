import chromadb

# -------------------
# CHROMADB CLIENT
# -------------------


client = chromadb.PersistentClient(path="./chroma_memory")

try:
    client.delete_collection(name="memory_collection")
except Exception:
    pass

collection = client.get_or_create_collection(name="memory_collection")

collection.add(
    documents=[
        "Percentage calculations use decimal multiplication.",
        "Current date returns the real system date.",
        "Text length counts characters in a string.",
    ],
    metadatas=[
        {
            "topic": "math",
            "type": "calculation",
        },
        {
            "topic": "date",
            "type": "system_info",
        },
        {
            "topic": "text",
            "type": "text_analysis",
        },
    ],
    ids=[
        "math",
        "date",
        "text",
    ],
)
results = collection.query(
    query_texts=["How do I calculate percentages?"],
    n_results=2,
)
print("\nCLEAN QUERY RESULTS:")

ids = results["ids"][0]
documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]

for i in range(len(ids)):
    print("\nResult", i + 1)
    print("ID:", ids[i])
    print("Topic:", metadatas[i]["topic"])
    print("Type:", metadatas[i]["type"])
    print("Document:", documents[i])
    print("Distance:", distances[i])
import chromadb

# -------------------
# CHROMADB CLIENT
# -------------------

# Creates a persistent ChromaDB database.
#
# Data is stored locally inside:
#
# ./chroma_memory/
#
# This allows the vector database to survive
# program restarts.

client = chromadb.PersistentClient(path="./chroma_memory")


# -------------------
# COLLECTION SETUP
# -------------------

# For learning purposes we delete and recreate
# the collection each run.
#
# In production systems you would normally use:
#
# - upsert()
# - update()
#
# instead of deleting data.

try:
    client.delete_collection(name="memory_collection")

except Exception:
    pass


# Create or retrieve a collection.
#
# A collection is conceptually similar to:
#
# - a table
# - a folder
# - a knowledge base

collection = client.get_or_create_collection(name="memory_collection")


# -------------------
# STORE DOCUMENTS
# -------------------

# Documents are automatically embedded by ChromaDB.
#
# Each document includes:
#
# - document text
# - metadata
# - unique id

collection.add(
    documents=[
        "Percentage calculations use decimal multiplication.",
        "Current date returns the real system date.",
        "Text length counts characters in a string.",
    ],
    metadatas=[
        {
            "topic": "math",
            "type": "calculation",
        },
        {
            "topic": "date",
            "type": "system_info",
        },
        {
            "topic": "text",
            "type": "text_analysis",
        },
    ],
    ids=[
        "math",
        "date",
        "text",
    ],
)


# -------------------
# VECTOR SEARCH
# -------------------

# ChromaDB:
#
# 1. Creates query embeddings
# 2. Compares against stored embeddings
# 3. Finds nearest vectors
# 4. Returns ranked results

results = collection.query(
    query_texts=["How do I calculate percentages?"],
    n_results=2,
)


# -------------------
# CLEAN RESULT DISPLAY
# -------------------

print("\nCLEAN QUERY RESULTS:")

ids = results["ids"][0]
documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


# -------------------
# DISPLAY RESULTS
# -------------------

for i in range(len(ids)):

    print("\nResult", i + 1)

    print("ID:", ids[i])

    print(
        "Topic:",
        metadatas[i]["topic"],
    )

    print(
        "Type:",
        metadatas[i]["type"],
    )

    print(
        "Document:",
        documents[i],
    )

    print(
        "Distance:",
        distances[i],
    )
