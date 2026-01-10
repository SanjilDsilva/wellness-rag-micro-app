from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path

from backend.db import init_db, log_interaction
from backend.safety import check_safety, unsafe_response
from backend.rag import query_rag


# Load environment variables explicitly from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Wellness RAG Micro-App")


@app.on_event("startup")
def startup_event():
    """
    Initialize MongoDB connection on app startup.
    """
    init_db()


@app.post("/ask")
def ask_question(payload: dict):
    """
    Main API endpoint for answering yoga & wellness questions.
    Applies safety checks before invoking RAG.
    """

    question = payload.get("question", "").strip()

    if not question:
        return {
            "answer": "Please provide a valid question.",
            "isUnsafe": False,
            "sources": []
        }

    # STEP 1: Safety check
    is_unsafe = check_safety(question)

    if is_unsafe:
        response = unsafe_response()

        log_interaction(
            query=question,
            is_unsafe=True,
            retrieved_chunks=[],
            response=response
        )

        return {
            "answer": response,
            "isUnsafe": True,
            "sources": []
        }

    # STEP 2: RAG pipeline (SAFE queries only)
    answer, sources = query_rag(question)

    log_interaction(
        query=question,
        is_unsafe=False,
        retrieved_chunks=[s["title"] for s in sources],
        response=answer
    )

    return {
        "answer": answer,
        "isUnsafe": False,
        "sources": sources
    }
