import json
import pickle
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import torch

# Force CPU usage to avoid CUDA compatibility issues
torch.cuda.is_available = lambda: False

from rag.config import (
    KB_FILE,
    INDEX_FILE,
    DOCS_FILE,
    META_FILE,
    EMBED_MODEL
)

print("Loading Vinci dataset...")

docs, metas = [], []
with open(KB_FILE, "r", encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)
        docs.append(row["text"])
        metas.append({"topic": row["topic"]})

print(f"Loaded {len(docs)} chunks")

print("Loading embedding model:", EMBED_MODEL)
encoder = SentenceTransformer(EMBED_MODEL)

emb_list = []
for i in tqdm(range(0, len(docs), 32), desc="Embedding"):
    batch = docs[i:i+32]
    vecs = encoder.encode(batch, convert_to_numpy=True)
    emb_list.append(vecs)

embeddings = np.vstack(emb_list).astype("float32")

print("Normalizing for cosine similarity...")
faiss.normalize_L2(embeddings)

print("Building FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(index, INDEX_FILE)
pickle.dump(docs, open(DOCS_FILE, "wb"))
pickle.dump(metas, open(META_FILE, "wb"))

print("FAISS index + metadata saved successfully!")