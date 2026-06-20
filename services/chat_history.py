from database.db import SessionLocal
from database.models import Message


def save_message(
    session_id: int,
    role: str,
    content: str
):
    db = SessionLocal()

    msg = Message(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(msg)
    db.commit()

    db.close()
    
    
def get_history(
    session_id: int,
    limit: int = 10
):

    db = SessionLocal()

    messages = (
        db.query(Message)
        .filter(
            Message.session_id == session_id
        )
        .order_by(Message.id.desc())
        .limit(limit)
        .all()
    )

    db.close()

    return list(
        reversed(messages)
    )