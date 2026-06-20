from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class PDF(Base):
    __tablename__ = "pdfs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(String)

    vector_path = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Session(Base):
    __tablename__ = "sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    pdf_id = Column(
        Integer,
        ForeignKey("pdfs.id")
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        Integer,
        ForeignKey("sessions.id")
    )
    
    role = Column(String)

    content = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )