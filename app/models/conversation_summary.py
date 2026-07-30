from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database.base import Base


class ConversationSummary(Base):
    __tablename__ = "conversation_summaries"

    id = Column(Integer, primary_key=True)

    customer_id = Column(String, index=True)

    summary = Column(Text)

    version = Column(Integer, default=1)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )