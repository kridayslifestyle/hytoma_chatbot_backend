from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer,String,Text

from app.database.base import Base


class ChatRequest(BaseModel):
    customer_id: str
    message: str


class ChatResponse(BaseModel):
    response: str

