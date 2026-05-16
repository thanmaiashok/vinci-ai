from rag.vinci_agent import ask_vinci

DEFAULT_MODEL = "llama3.1:8b-instruct-q4_K_M"

def vinci_answer(query: str, model: str = DEFAULT_MODEL):
    """
    Calls the Vinci RAG engine and returns the model's response.
    """
    try:
        answer = ask_vinci(query, model=model)
        return {
            "success": True,
            "model": model,
            "query": query,
            "answer": answer
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }