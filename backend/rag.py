import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


DATA_PATH = Path(__file__).parent / "data" / "yoga_knowledge.json"

vectorstore = None


def load_documents():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    for item in data:
        content = (
            f"Title: {item['title']}\n"
            f"Category: {item['category']}\n"
            f"Description: {item['description']}\n"
            f"Benefits: {item['benefits']}\n"
            f"Contraindications: {item['contraindications']}\n"
            f"Level: {item['level']}\n"
            f"Source: {item['source']}"
        )

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "title": item["title"],
                    "source": item["source"],
                    "category": item["category"]
                }
            )
        )

    return documents


def init_vectorstore():
    global vectorstore

    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    split_docs = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(split_docs, embeddings)


def query_rag(question: str):
    if vectorstore is None:
        init_vectorstore()

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a yoga and wellness assistant.\n"
            "Answer the question using ONLY the provided context.\n"
            "If the answer is not present in the context, say \"I don't know.\".\n"
            "Do NOT provide medical advice.\n\n"
            "Context:\n{context}\n\n"
            "Question:\n{question}\n\n"
            "Answer:"
        )
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    answer = llm.invoke(
        prompt.format(context=context, question=question)
    ).content

    sources = [
        {
            "title": doc.metadata.get("title"),
            "source": doc.metadata.get("source")
        }
        for doc in retrieved_docs
    ]

    return answer, sources
