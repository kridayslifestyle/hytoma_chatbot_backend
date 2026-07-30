from sqlalchemy import Column, Integer, String, Text
from app.database.base import Base


class CustomerProfile(Base):

    __tablename__ = "customer_profiles"

    id = Column(
        Integer,
        primary_key=True
    )

    customer_uid = Column(
        String,
        unique=True,
        index=True
    )

    budget = Column(String)

    preferred_color = Column(String)

    ecosystem = Column(String)

    interests = Column(Text)

    location = Column(String)

    last_purchase = Column(String)