# Day 20 — ChromaDB Vector Database

## Objective

Day 20 focused on building the first real vector database system capable of:

- vector storage
- embedding storage
- semantic search
- metadata storage
- nearest-neighbor retrieval
- vector ranking
- persistent vector databases

The goal was to move beyond toy memory systems and begin using a production-grade vector database capable of storing and retrieving knowledge using embeddings.

---

# Core Lesson

Day 19 introduced:

```text
Text
↓
Embedding
↓
Vector
↓
Distance
↓
Best Match
```

Day 20 introduced:

```text
Document
↓
Embedding
↓
Vector Database
↓
Similarity Search
↓
Best Match
```

This became the first true:

```text
Production Retrieval Architecture
```

---

# Day 20 Architecture

```text
Document
      ↓
Embedding
      ↓
ChromaDB Collection
      ↓
Vector Storage
      ↓
Similarity Search
      ↓
Ranked Results
      ↓
Best Match
```

This architecture introduced real-world vector retrieval.

---

# Why Day 20 Matters

Day 16:

```text
Persistent Memory
```

Day 17:

```text
Memory Ranking
```

Day 18:

```text
Semantic Retrieval
```

Day 19:

```text
Embeddings
```

Day 20:

```text
Vector Database
```

This is the point where the learning journey transitions from:

```text
Learning Architectures
```

to:

```text
Using Real Retrieval Systems
```

---

# What Is ChromaDB?

ChromaDB is a:

```text
Vector Database
```

Instead of storing:

```python
{
    "topic": "math",
    "content": "Percentage calculations..."
}
```

it stores:

```text
Document
+
Embedding
+
Metadata
```

and performs:

```text
Similarity Search
```

automatically.

---

# ChromaDB Client

Day 20 introduced:

```python
chromadb.PersistentClient()
```

Example:

```python
client = chromadb.PersistentClient(
    path="./chroma_memory"
)
```

Purpose:

- persist vector database to disk
- survive program restarts
- store embeddings permanently

This became the first:

```text
Persistent Vector Database
```

---

# ChromaDB Collection

Day 20 introduced:

```python
collection = client.get_or_create_collection()
```

Example:

```python
collection = client.get_or_create_collection(
    name="memory_collection"
)
```

Purpose:

- organize documents
- organize embeddings
- provide searchable knowledge

A collection is conceptually similar to:

```text
Table
Folder
Knowledge Base
```

---

# Document Storage

Day 20 introduced:

```python
collection.add()
```

Example:

```python
collection.add(
    documents=[
        "Percentage calculations use decimal multiplication.",
        "Current date returns the real system date.",
        "Text length counts characters in a string.",
    ]
)
```

Purpose:

- store knowledge
- create embeddings automatically
- support future retrieval

---

# Metadata Storage

One of the most important Day 20 improvements was:

```python
metadatas=[]
```

Example:

```python
{
    "topic": "math",
    "type": "calculation",
}
```

Purpose:

- categorize documents
- improve search results
- support filtering

This introduced:

```text
Structured Knowledge Storage
```

---

# Automatic Embeddings

Unlike Day 19:

```python
create_embedding()
```

Day 20 introduced:

```text
Automatic Embedding Generation
```

ChromaDB automatically:

```text
Document
↓
Embedding
↓
Storage
```

without requiring manual vector creation.

---

# Similarity Search

Day 20 introduced:

```python
collection.query()
```

Example:

```python
collection.query(
    query_texts=[
        "How do I calculate percentages?"
    ]
)
```

Purpose:

- create query embedding
- compare with stored embeddings
- retrieve nearest matches

This became the first:

```text
Vector Search Engine
```

---

# Vector Ranking

The workflow introduced:

```text
Query Embedding
↓
Stored Embeddings
↓
Distance Calculation
↓
Ranking
```

Result:

```text
math
↓
closest match
```

because:

```text
How do I calculate percentages?
```

is semantically related to:

```text
Percentage calculations use decimal multiplication.
```

---

# Distance Scores

Day 20 introduced:

```text
Distance
```

Example:

```text
math
0.4668

text
1.8057
```

Interpretation:

```text
Lower Distance
=
Closer Meaning
```

Therefore:

```text
math
```

was selected as the best result.

---

# Clean Result Display

Day 20 introduced:

```text
ID
Topic
Type
Document
Distance
```

Example:

```text
Result 1

ID: math

Topic: math

Type: calculation

Distance: 0.4668
```

This became the first:

```text
Readable Retrieval Output
```

---

# Persistent Storage

Day 20 introduced:

```text
chroma_memory/
```

Example:

```text
chroma.sqlite3
```

Purpose:

- store vectors on disk
- survive restarts
- support long-term knowledge

This became the first:

```text
Persistent Vector Knowledge Base
```

---

# ChromaDB Workflow

```text
Document
      ↓
Embedding
      ↓
Collection
      ↓
Vector Database
      ↓
Similarity Search
      ↓
Best Match
```

This is very similar to:

- RAG systems
- ChatGPT memory
- enterprise AI search
- semantic search engines

---

# Example Workflow

## Step 1

Create collection.

Result:

```text
memory_collection
```

---

## Step 2

Store documents.

Result:

```text
math
date
text
```

---

## Step 3

Store metadata.

Result:

```text
topic
type
```

---

## Step 4

Query collection.

Example:

```text
How do I calculate percentages?
```

---

## Step 5

Generate embeddings.

Result:

```text
Automatic
```

---

## Step 6

Perform similarity search.

Result:

```text
math
```

returned first.

---

# Key Concepts Learned

- vector databases
- ChromaDB
- collections
- metadata
- automatic embeddings
- similarity search
- vector ranking
- nearest-neighbor retrieval
- persistent vector storage

---

# Most Important Insights

## 1. Embeddings Need A Database

Day 19 created vectors.

Day 20 stored vectors.

---

## 2. Similarity Search Is The Foundation Of RAG

Modern retrieval systems work by:

```text
Embedding
↓
Similarity Search
↓
Best Match
```

---

## 3. Metadata Makes Retrieval More Useful

Documents become easier to understand and organize when metadata is attached.

---

## 4. Persistence Matters

Knowledge should survive application restarts.

ChromaDB provides:

```text
Persistent Vector Storage
```

---

# Example Final Output

```text
CLEAN QUERY RESULTS:

Result 1

ID: math
Topic: math
Type: calculation

Document:
Percentage calculations use decimal multiplication.

Distance:
0.4668

Result 2

ID: text
Topic: text
Type: text_analysis

Distance:
1.8057
```

---

# Technologies Used

- Python
- ChromaDB
- Vector Databases
- Embeddings
- Metadata
- Similarity Search
- Persistent Storage

---

# Future Improvements

Possible next improvements:

- larger knowledge bases
- document chunking
- retrieval-augmented generation
- hybrid search
- production RAG systems
- LangChain
- LlamaIndex

---

# Most Important Day 20 Insight

```text
A vector database transforms embeddings into a searchable knowledge system.

Embeddings represent meaning.
Vector databases make that meaning retrievable.
```