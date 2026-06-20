import uuid
import os
from database.db import SessionLocal
from database.models import PDF
from database.models import Session
from database.db import SessionLocal
from database.models import Message
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from services.pdf_loader import load_pdf
from services.vector_store import (
    split_docs,
    create_vector_db
)
from services.rag import ask_question
from database.db import engine
from database.models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/upload")

# async def upload_pdf(
#     file: UploadFile
# ):

#     path = f"uploads/{file.filename}"

#     with open(path, "wb") as f:
#         f.write(
#             await file.read()
#         )

#     docs = load_pdf(path)

#     chunks = split_docs(docs)

#     create_vector_db(chunks)

#     return {
#         "message":
#         "PDF processed"
#     }

@app.post("/upload")
async def upload_pdf(
    file: UploadFile
):

    db = SessionLocal()

    pdf_uuid = str(uuid.uuid4())

    upload_path = f"uploads/{pdf_uuid}_{file.filename}"

    with open(upload_path, "wb") as f:
        f.write(
            await file.read()
        )

    docs = load_pdf(upload_path)

    chunks = split_docs(docs)

    vector_path = f"vector_db/{pdf_uuid}"

    os.makedirs(
        vector_path,
        exist_ok=True
    )

    create_vector_db(
        chunks,
        vector_path
    )

    pdf = PDF(
        filename=file.filename,
        vector_path=vector_path
    )

    db.add(pdf)
    db.commit()
    db.refresh(pdf)

    return {
        "pdf_id": pdf.id,
        "filename": file.filename
    }

@app.get("/ask")
def ask(
    session_id: int,
    q: str
):

    answer = ask_question(
        session_id,
        q
    )

    return {
        "answer": answer
    }
    
@app.post("/session/{pdf_id}")
def create_session(pdf_id: int):

    db = SessionLocal()

    pdf = db.query(PDF).filter(
        PDF.id == pdf_id
    ).first()

    if not pdf:
        return {
            "error": "PDF not found"
        }

    session = Session(
        pdf_id=pdf_id
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id,
        "pdf_id": pdf_id
    }
    
@app.get("/history/{session_id}")
def history(
    session_id: int
):

    db = SessionLocal()

    messages = (
        db.query(Message)
        .filter(
            Message.session_id == session_id
        )
        .all()
    )

    return messages
@app.get("/pdfs")
def get_pdfs():

    db = SessionLocal()

    try:
        pdfs = db.query(PDF).all()

        return [
            {
                "id": pdf.id,
                "name": pdf.filename,
            }
            for pdf in pdfs
        ]

    finally:
        db.close()
