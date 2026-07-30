from sqlalchemy import Column, Integer, String
from app.database.base import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_uid = Column(
        String,
        unique=True,
        index=True
    )

    name = Column(String)

    phone = Column(String)

    email = Column(String)