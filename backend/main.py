from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from backend.db import init_db
from backend.safety import check_safety, unsafe_response
from backend.db import log_interaction


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Wellness RAG Micro-App")


@app.on_event("startup")
def startup_event():
    init_db()


@app.post("/ask")
def ask_question(payload: dict):
    question = payload.get("question", "")

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

    # SAFE queries will go to RAG later
    return {
        "answer": "Safe query placeholder",
        "isUnsafe": False,
        "sources": []
    }
