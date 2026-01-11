# Frontend – Wellness RAG Micro-App

This is the minimal frontend for the **Wellness RAG Micro-App**.

## Purpose

The frontend provides a simple, calming interface for users to:

* Ask yoga and wellness-related questions
* View AI-generated answers
* See which sources were used (RAG transparency)
* Notice safety warnings for sensitive queries

The design intentionally avoids complexity and focuses on **clarity, calmness, and trust**.

---

## Tech Stack

* HTML
* CSS
* Vanilla JavaScript

No frontend frameworks were used to keep the system lightweight and easy to evaluate.

---

## Features

* Question input box
* “Ask” button
* Loading indicator
* Answer display
* Source attribution section
* Safety warning block (shown only when applicable)

---

## Backend Connection

The frontend communicates with the backend via:

```
POST http://127.0.0.1:8000/ask
```

Ensure the backend is running before using the frontend.

---

## How to Run

1. Start the backend:

```bash
uvicorn backend.main:app --reload
```

2. Open `index.html` directly in a browser
   (or use VS Code Live Server).

---

## Design Notes

* Soft, wellness-inspired color palette
* Large readable typography
* Minimal distractions
* Focus on user comfort and trust

This frontend is intentionally simple — the evaluation focus is on **RAG quality, safety, and system design**, not UI complexity.
