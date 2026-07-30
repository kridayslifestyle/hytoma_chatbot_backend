from sqlalchemy.orm import Session
from app.models.conversation import Conversation


def save_message(db, customer_id, role, message):

    try:
        conversation = Conversation(
            customer_id=customer_id,
            role=role,
            message=message
        )

        db.add(conversation)
        db.commit()

    except Exception as e:
        db.rollback()   # 🔥 CRITICAL
        print("SAVE MESSAGE ERROR:", e)


def get_history(
        db,
        customer_id,
        limit=10):

    messages = (
        db.query(Conversation)
        .filter(
            Conversation.customer_id == customer_id
        )
        .order_by(
            Conversation.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    messages.reverse()

    return messages