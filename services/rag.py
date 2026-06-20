from langchain_community.vectorstores import FAISS
from services.embeddings import get_embeddings
from database.db import SessionLocal
from database.models import Session, PDF

from services.chat_history import (
    save_message,
    get_history
)

from services.query_rewriter import (
    rewrite_question
)

from services.llm import llm


def ask_question(
    session_id: int,
    question: str
):
    db_session = SessionLocal()

    try:
        # -----------------------------
        # Validate Session
        # -----------------------------
        session = (
            db_session.query(Session)
            .filter(Session.id == session_id)
            .first()
        )

        if not session:
            return "Session not found"

        # -----------------------------
        # Get PDF
        # -----------------------------
        pdf = (
            db_session.query(PDF)
            .filter(PDF.id == session.pdf_id)
            .first()
        )

        if not pdf:
            return "PDF not found"

        # -----------------------------
        # Load Previous History
        # -----------------------------
        history = get_history(
            session_id,
            limit=10
        )

        history_text = "\n".join(
            f"{msg.role}: {msg.content}"
            for msg in history
        )

        # -----------------------------
        # Rewrite Question
        # -----------------------------
        rewritten_question = rewrite_question(
            history_text,
            question
        )

        print("\n====================")
        print("Original Question:")
        print(question)

        print("\nRewritten Question:")
        print(rewritten_question)
        print("====================\n")

        # -----------------------------
        # Save User Question
        # -----------------------------
        save_message(
            session_id,
            "user",
            question
        )

        # -----------------------------
        # Load Embeddings
        # -----------------------------
        # embeddings = HuggingFaceEmbeddings(
        #     model_name="sentence-transformers/all-MiniLM-L6-v2"
        # )

        # -----------------------------
        # Load Correct Vector DB
        # -----------------------------
        vector_db = FAISS.load_local(
            pdf.vector_path,
            get_embeddings(),
            allow_dangerous_deserialization=True
        )

        # -----------------------------
        # Retrieve Relevant Chunks
        # -----------------------------
        docs = vector_db.similarity_search(
            rewritten_question,
            k=3
        )

        context = "\n".join(
            doc.page_content
            for doc in docs
        )

        # -----------------------------
        # Prompt
        # -----------------------------
        prompt = f"""
You are a PDF assistant.

Answer ONLY from the provided context.

If the answer is not present in the context,
reply exactly:

"I could not find this information in the uploaded PDF."

Chat History:
{history_text}

Context:
{context}

Question:
{question}
"""

        # -----------------------------
        # Generate Answer
        # -----------------------------
        result = llm.invoke(prompt)

        answer = result.content

        # -----------------------------
        # Save Assistant Response
        # -----------------------------
        save_message(
            session_id,
            "assistant",
            answer
        )

        return answer

    finally:
        db_session.close()
