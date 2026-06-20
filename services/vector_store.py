import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from services.embeddings import get_embeddings



def split_docs(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_documents(documents)


def create_vector_db(
    chunks,
    vector_path
):

    db = FAISS.from_documents(
        chunks,
        get_embeddings()
    )

    db.save_local(vector_path)

    return db
