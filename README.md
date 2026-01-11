# Wellness RAG Micro-App – “Ask Me Anything About Yoga”

## Project Overview

This project is a full-stack AI-powered micro-application built as part of the **NextYou Wellness RAG Challenge**.

The application answers yoga and wellness-related questions using a **Retrieval-Augmented Generation (RAG)** pipeline, with a strong emphasis on:

* Safety-first responses for health-related queries
* Transparent source attribution
* Clean backend architecture
* Structured data logging for analysis

The goal is not just to generate answers, but to do so **responsibly**, **explainably**, and **reliably**.

---

## Core Features

* Ask natural language questions about yoga and wellness
* RAG-based answers grounded in a curated knowledge base
* Clear display of retrieved sources
* Safety detection for risky queries (medical conditions, pregnancy, etc.)
* MongoDB logging of:

  * User queries
  * Retrieved chunks
  * Final answers
  * Safety flags
  * Timestamps
* Minimal, calming frontend UI focused on clarity

---

## Tech Stack

### Frontend

* HTML, CSS, JavaScript
* Minimal UI with focus on readability and calm color psychology
* Displays:

  * Answer
  * Source attribution
  * Safety warnings (when applicable)

### Backend

* **FastAPI (Python)**
* Modular structure:

  * `main.py` – API routes
  * `rag.py` – RAG pipeline
  * `safety.py` – safety detection & guardrails
  * `db.py` – MongoDB connection and logging

### AI & RAG

* Vector Store: **FAISS (local)**
* Embeddings: **HuggingFace sentence-transformers**
* LLM: **Google Gemini (gemini-2.5-flash)**
* Chunking: Recursive character-based splitting
* Prompting: Context-aware answer generation using retrieved chunks only

### Database

* **MongoDB**
* Used for storing:

  * Query text
  * Retrieved document metadata
  * Model responses
  * Safety flags
  * Timestamps

---

## RAG Pipeline (High-Level)

1. User submits a question
2. Safety layer checks for risky intent
3. If unsafe:

   * Skip RAG
   * Return safety-first response
   * Log interaction
4. If safe:

   * Load and chunk knowledge base
   * Generate embeddings
   * Retrieve top relevant chunks from FAISS
   * Construct context-aware prompt
   * Generate answer via Gemini
   * Return answer + sources
   * Log interaction in MongoDB

---

## Safety Logic

The system flags queries that mention:

* Pregnancy
* Medical conditions (e.g. hernia, glaucoma, high BP)
* Recent surgery or physical risk

When flagged:

* No medical advice is given
* A gentle warning is displayed
* Safer alternatives are suggested
* Professional consultation is recommended
* `isUnsafe = true` is stored in MongoDB

This ensures the system remains **informational**, not **prescriptive**.

---

## API Endpoints

### `POST /ask`

**Request**

```json
{
  "question": "What are the benefits of Surya Namaskar?"
}
```

**Response**

```json
{
  "answer": "...",
  "isUnsafe": false,
  "sources": [
    { "title": "Surya Namaskar", "source": "Yoga Journal" }
  ]
}
```

---

## Running Locally

### Prerequisites

* Python 3.11
* MongoDB (local or Atlas)
* Virtual environment

### Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```
MONGODB_URI=your_mongodb_uri
GOOGLE_API_KEY=your_gemini_api_key
```

Run the backend:

```bash
uvicorn backend.main:app --reload
```

Open API docs:

```
http://127.0.0.1:8000/docs
```

---

## APK

A tested Android APK is included for mobile evaluation.
See `apk/README.md` for details.

---

## Design Decisions

* Focused on correctness and safety over UI complexity
* Used local FAISS for simplicity and transparency
* Avoided medical advice by design
* Logged all interactions for observability and analysis

---

## Demo

A 2–5 minute demo video is included covering:

* RAG flow
* Safety handling
* UI walkthrough

---

## Author

**Sanjil Cleetus D’silva**

---

This project was built to demonstrate real-world RAG system design, not just framework usage.
