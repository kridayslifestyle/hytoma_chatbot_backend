from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database.base import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(String, index=True)

    role = Column(String)
    message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)