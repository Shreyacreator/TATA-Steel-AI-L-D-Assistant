import os
import numpy as np
import faiss
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdfs(folder_path="knowledge_base"):
    texts = []

    if not os.path.exists(folder_path):
        return []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            try:
                reader = PdfReader(path)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                if text.strip():
                    texts.append(text)
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return texts



def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks



def build_vector_store(folder_path="knowledge_base"):
    pdf_texts = extract_text_from_pdfs(folder_path)

    all_chunks = []
    for text in pdf_texts:
        all_chunks.extend(chunk_text(text))

    if not all_chunks:
        return None, []

    embeddings = EMBED_MODEL.encode(all_chunks)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, all_chunks



def retrieve_context(query, index, chunks, top_k=3):
    if index is None or not chunks:
        return ""

    query_embedding = EMBED_MODEL.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(chunks):
            results.append(chunks[idx])

    return "\n\n".join(results)