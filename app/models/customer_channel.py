from sqlalchemy import Column, Integer, String
from app.database.base import Base


class CustomerChannel(Base):

    __tablename__ = "customer_channels"

    id = Column(
        Integer,
        primary_key=True
    )

    customer_uid = Column(
        String,
        index=True
    )

    platform = Column(
        String
    )

    platform_user_id = Column(
        String,
        unique=True
    )