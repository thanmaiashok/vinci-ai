import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

# Force CPU usage to avoid CUDA compatibility issues
torch.cuda.is_available = lambda: False

from rag.config import (
    INDEX_FILE,
    DOCS_FILE,
    META_FILE,
    EMBED_MODEL,
    TOP_K
)

# Global variables for lazy loading
_index = None
docs = None
metas = None
encoder = None


def _load_resources():
    """Load FAISS index and metadata lazily."""
    global _index, docs, metas, encoder
    
    if _index is None:
        print("Loading FAISS index + metadata...")
        _index = faiss.read_index(INDEX_FILE)
        docs = pickle.load(open(DOCS_FILE, "rb"))
        metas = pickle.load(open(META_FILE, "rb"))
        encoder = SentenceTransformer(EMBED_MODEL)


def retrieve_chunks(query: str):
    """Return the top-K most relevant Vinci notebook passages."""
    _load_resources()
    
    q_emb = encoder.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(q_emb)

    sims, idxs = _index.search(q_emb, TOP_K)

    results = []
    for score, i in zip(sims[0], idxs[0]):
        results.append({
            "score": float(score),
            "text": docs[i],
            "topic": metas[i]["topic"]
        })
    return results