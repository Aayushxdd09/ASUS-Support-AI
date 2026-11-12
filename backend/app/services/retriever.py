
import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[3]

VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"

INDEX_FILE = VECTOR_STORE_DIR / "asus_index.faiss"
CHUNKS_FILE = VECTOR_STORE_DIR / "chunks.json"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# Load embedding model
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Load FAISS index
index = faiss.read_index(str(INDEX_FILE))

# Load original chunks
with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
    chunks = json.load(file)


def retrieve_documents(query, top_k=3):

    # Convert user question into embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Search FAISS
    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        results.append({
            "text": chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "score": float(score)
        })

    return results


if __name__ == "__main__":

    question = "Why is my ASUS laptop keyboard backlight not working?"

    results = retrieve_documents(question)

    print(f"\nQuestion: {question}")

    for result in results:
        print("\nSource:", result["source"])
        print("Similarity:", round(result["score"], 3))
        print("Content:", result["text"][:500])
