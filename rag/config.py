import os

# Project root (two levels up from this file: rag/ -> project root)
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to your labeled Vinci dataset
KB_FILE = os.path.join(_BASE, "data", "vinci_labeled.jsonl")

# Output files created after building the KB index
INDEX_FILE = os.path.join(_BASE, "data", "vinci_index.faiss")
DOCS_FILE  = os.path.join(_BASE, "data", "docs.pkl")
META_FILE  = os.path.join(_BASE, "data", "metas.pkl")

# Embedding model for vector generation
# all-MiniLM-L6-v2 is fast and accurate for semantic similarity
EMBED_MODEL = "all-MiniLM-L6-v2"

# Number of chunks to retrieve during querying
TOP_K = 5
