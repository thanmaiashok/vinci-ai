# rag/vinci_agent.py

from rag.query_rag import retrieve_chunks
from rag.ollama_client import ollama_chat

# Words that should NOT trigger RAG retrieval
GREETINGS = ["hi", "hello", "hey", "yo", "sup", "hola", "hii", "hiii", "heyy"]

NOTEBOOK_TOPICS = [
    "water", "river", "flow", "fluid",
    "light", "shadow", "optics",
    "painting", "art", "color",
    "geometry", "line", "shape",
    "mechanics", "machine", "motion",
    "anatomy", "body", "muscle", "bone",
    "nature", "plants", "animals",
    "architecture", "town", "building",
    "engineering", "bridge"
]

def is_smalltalk(user_text: str):
    text = user_text.lower().strip()

    # direct greeting
    if text in GREETINGS:
        return True

    # ≤ 2 words with no question mark → probably not a real query
    if len(text.split()) <= 2 and "?" not in text:
        return True

    # very short text like "ok", "yo", "hm"
    if len(text) <= 3:
        return True

    return False

def is_notebook_question(q: str):
    q = q.lower()
    return any(word in q for word in NOTEBOOK_TOPICS)

def smalltalk_response(query: str, model="llama3.1:8b-instruct-q4_K_M"):
    """Converts greetings into SHORT clean replies."""
    messages = [
        {"role": "system", "content": (
            "You are Vinci. For greetings or small talk, ALWAYS reply briefly and politely. "
            "Do NOT use historical notes. Do NOT analyze. Do NOT write long paragraphs. "
            "Keep responses clean and well-aligned."
        )},
        {"role": "user", "content": query}
    ]
    try:
        return ollama_chat(model, messages)
    except Exception as e:
        # Fallback response if Ollama is not available
        return "Hello! I'm Vinci, your Leonardo-inspired assistant. How can I help you today?"


def build_prompt(query: str, chunks: list):
    """Clean structured prompt for real questions."""
    context_block = "\n\n".join(
        [f"[{c['topic']}] {c['text']}" for c in chunks]
    )

    return f"""
You are VINCI — a reasoning engine inspired by Leonardo da Vinci.
Your answers MUST be:

- Clean and well-aligned
- Use proper bullet points (•) not asterisks (*)
- Keep each point concise and clear
- Organize information logically
- NO long essays or irrelevant notes

CONTEXT (from notebooks):
{context_block}

QUESTION:
{query}

RULES:
1. Use ONLY the context above.
2. Format output using proper bullet points (•) for lists.
3. If the notes do not answer, say:
   \"No direct note found; here is a brief inference:\"
4. LIMIT answers to 6–8 lines MAX.
5. Ensure all responses are well-aligned and properly formatted with consistent indentation.
"""

def ask_vinci(query: str, model="llama3.1:8b-instruct-q4_K_M"):

    # 1) Small talk → NO RAG
    if is_smalltalk(query):
        return smalltalk_response(query, model)

    # 2) If question has NOTHING to do with Leonardo topics → NO RAG
    if not is_notebook_question(query):
        messages = [
            {"role": "system", "content": (
                "You are Vinci. Give clean, short, wise, modern answers. "
                "Do NOT reference Leonardo's notes unless the question is about art, science, anatomy, mechanics, water, optics, geometry, or nature. "
                "Keep responses well-aligned and properly formatted. "
                "Use proper bullet points (•) not asterisks (*) for lists. "
                "Do NOT use markdown formatting like **bold** or *italic*. "
                "Ensure each bullet point is on its own line with consistent indentation. "
                "Limit lists to 8 items maximum."
            )},
            {"role": "user", "content": query}
        ]
        try:
            return ollama_chat(model, messages)
        except Exception as e:
            # Fallback response if Ollama is not available
            return "I'm Vinci, your Leonardo-inspired assistant. I can help you with:\n\n• Art and painting techniques\n• Science and engineering principles\n• Human anatomy and physiology\n• Mechanical designs and inventions\n• Water flow and fluid dynamics\n• Optical phenomena and light\n• Geometric principles and forms\n• Natural observations and botany\n\nWhich area interests you most?"

    # 3) If question is related → use RAG
    chunks = retrieve_chunks(query)

    # If RAG fails → fallback
    if chunks is None or len(chunks) == 0:
        messages = [
            {"role": "system", "content": "You are Vinci. Give a clean, short, thoughtful answer. Keep responses well-aligned."},
            {"role": "user", "content": query}
        ]
        try:
            return ollama_chat(model, messages)
        except Exception as e:
            # Fallback response if Ollama is not available
            return "I'm Vinci, your Leonardo-inspired assistant. I couldn't find specific notes about that, but I can help with:\n\n• Art and painting techniques\n• Science and engineering principles\n• Human anatomy and physiology\n• Mechanical designs and inventions\n• Water flow and fluid dynamics\n• Optical phenomena and light\n• Geometric principles and forms\n• Natural observations and botany\n\nWhat would you like to explore?"

    # Build structured Vinci prompt
    prompt = build_prompt(query, chunks)
    messages = [
        {"role": "system", "content": "You are Vinci, reasoning using notebook context. Keep responses well-aligned and properly formatted."},
        {"role": "user", "content": prompt}
    ]
    try:
        return ollama_chat(model, messages)
    except Exception as e:
        # Fallback response if Ollama is not available
        return "I'm Vinci, your Leonardo-inspired assistant. I'm having trouble accessing my knowledge base right now, but I can help with:\n\n• Art and painting techniques\n• Science and engineering principles\n• Human anatomy and physiology\n• Mechanical designs and inventions\n• Water flow and fluid dynamics\n• Optical phenomena and light\n• Geometric principles and forms\n• Natural observations and botany\n\nWhat area would you like to discuss?"