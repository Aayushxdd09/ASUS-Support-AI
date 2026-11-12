
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DOCUMENTS_FOLDER = PROJECT_ROOT / "data" / "processed"


def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into overlapping chunks.

    chunk_size: number of words per chunk
    overlap: number of words shared between chunks
    """

    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = words[start:end]

        chunks.append(" ".join(chunk))

        # Move forward while keeping some overlap
        start += chunk_size - overlap

    return chunks


def load_and_chunk_documents():

    all_chunks = []

    for file_path in DOCUMENTS_FOLDER.glob("document_*.txt"):

        text = file_path.read_text(encoding="utf-8")

        chunks = chunk_text(text)

        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "source": file_path.name
            })

    return all_chunks


if __name__ == "__main__":

    chunks = load_and_chunk_documents()

    print(f"Total chunks created: {len(chunks)}")

    if chunks:
        print("\nFirst chunk:")
        print(chunks[0]["text"])
