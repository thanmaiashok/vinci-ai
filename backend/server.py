from fastapi import FastAPI, Query
from backend.llm_client import vinci_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Vinci Reasoning API")

# Enable CORS (frontend needs this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask")
def ask_endpoint(q: str = Query(..., description="User question")):
    """
    Ask the Vinci RAG engine a question.
    """
    return vinci_answer(q)

@app.get("/")
def root():
    return {
        "message": "Vinci Reasoning Engine is running. Use /ask?q=your-question"
    }