
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from backend.app.services.chunker import load_and_chunk_documents


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[3]
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"

INDEX_FILE = VECTOR_STORE_DIR / "asus_index.faiss"
CHUNKS_FILE = VECTOR_STORE_DIR / "chunks.json"


# Free local embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def build_vector_store():

    print("Loading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("Loading document chunks...")

    chunks = load_and_chunk_documents()

    if not chunks:
        raise ValueError("No document chunks found!")

    # Extract text from chunks
    texts = [chunk["text"] for chunk in chunks]

    print(f"Generating embeddings for {len(texts)} chunks...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    # Convert embeddings to float32 for FAISS
    embeddings = np.asarray(embeddings, dtype="float32")

    # Create FAISS index
    embedding_dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(embedding_dimension)

    # Add vectors to index
    index.add(embeddings)

    # Create storage directory
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, str(INDEX_FILE))

    # Save original chunks and their source filenames
    with open(CHUNKS_FILE, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)

    print("\nVector store created successfully!")
    print(f"Total vectors: {index.ntotal}")
    print(f"Embedding dimensions: {embedding_dimension}")
    print(f"Saved index: {INDEX_FILE}")
    print(f"Saved chunks: {CHUNKS_FILE}")


if __name__ == "__main__":
    build_vector_store()
