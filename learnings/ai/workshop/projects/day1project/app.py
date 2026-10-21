"""Ask questions about a PDF using local embedding retrieval and an LLM."""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


def extract_pdf_text(pdf_path):
    """Read text from every page in a text-based PDF."""
    reader = PdfReader(pdf_path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def make_chunks(text, chunk_size=120, overlap=30):
    """Split text into word chunks with a little repeated context."""
    words = text.split()
    if not words:
        return []
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks


def embed_chunks(model, chunks):
    """Convert passages into vectors for meaning-based search."""
    return model.encode(chunks, normalize_embeddings=True)


def retrieve(model, chunks, chunk_vectors, question, top_k=3):
    """Return the most similar passages and their similarity scores."""
    question_vector = model.encode([question], normalize_embeddings=True)[0]
    # Vectors are normalized, so their dot product is cosine similarity.
    scores = chunk_vectors @ question_vector
    best_indexes = sorted(range(len(chunks)), key=lambda i: float(scores[i]), reverse=True)
    return [(chunks[i], float(scores[i])) for i in best_indexes[:top_k]]


def ask_model(question, passages):
    """Send the question and retrieved source text to OpenRouter."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Set the OPENROUTER_API_KEY environment variable first.")

    model_name = os.getenv("OPENROUTER_MODEL", "openrouter/free")
    context = "\n\n".join(
        f"Source {index}: {text}" for index, (text, _score) in enumerate(passages, start=1)
    )
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Answer using only the supplied PDF passages. If they do not contain "
                    "the answer, say: I could not find that in the PDF. Keep the answer concise."
                ),
            },
            {
                "role": "user",
                "content": f"PDF passages:\n{context}\n\nQuestion: {question}",
            },
        ],
        "temperature": 0,
    }
    request = Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"The model service returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach the model service: {error.reason}") from error

    return result["choices"][0]["message"]["content"].strip()


def main():
    if len(sys.argv) != 2:
        print('Usage: python app.py "path/to/document.pdf"')
        return

    pdf_path = sys.argv[1]
    if not os.path.isfile(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    text = extract_pdf_text(pdf_path)
    if not text:
        print("No selectable text found. This may be a scanned PDF that needs OCR.")
        return

    chunks = make_chunks(text)
    print(f"Read PDF and created {len(chunks)} chunks.")
    print("Loading embedding model (the first run may download it)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunk_vectors = embed_chunks(model, chunks)

    while True:
        question = input("\nQuestion (or 'quit'): ").strip()
        if question.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        if not question:
            continue

        passages = retrieve(model, chunks, chunk_vectors, question)
        try:
            answer = ask_model(question, passages)
        except (RuntimeError, KeyError, IndexError) as error:
            print(f"\nCould not get an answer: {error}")
            continue

        print(f"\nAnswer: {answer}")
        print("\nRetrieved passages (check these against the answer):")
        for index, (passage, score) in enumerate(passages, start=1):
            print(f"[{index}; similarity {score:.2f}] {passage}")


if __name__ == "__main__":
    main()
