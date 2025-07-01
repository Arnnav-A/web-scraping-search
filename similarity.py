import os
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

INDEX_PATH = "cache/query_index"

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

faiss_index = None
if os.path.exists(INDEX_PATH):
    faiss_index = FAISS.load_local(INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)

def save_faiss_index():
    if faiss_index:
        os.makedirs(INDEX_PATH, exist_ok=True)
        faiss_index.save_local(INDEX_PATH)

def get_similar_query(query: str, threshold: float = 1) -> str | None:
    """
    Search for a similar query in the index.
    Returns the cached answer if similarity score is above threshold, else None.
    """
    if faiss_index is None:
        return None

    results = faiss_index.similarity_search_with_score(query, k=1)
    if results:
        doc, score = results[0]
        if score < threshold:
            return doc.metadata.get("answer", None)
    return None

def add_query_result(query: str, answer: str) -> None:
    """
    Add the query and answer to the index and save.
    """
    global faiss_index
    if not faiss_index:
        faiss_index = FAISS.from_texts([query], embedding_model, metadatas=[{"answer": answer}])
    else:
        faiss_index.add_texts([query], metadatas=[{"answer": answer}])
    save_faiss_index()
