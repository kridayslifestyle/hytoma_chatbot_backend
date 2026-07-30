from app.database.connection import engine
from app.database.base import Base

# import models
from app.models.customer import Customer
from app.models.conversation import Conversation
from app.models.conversation_summary import ConversationSummary
from app.models.customer_channel import CustomerChannel
from app.models.customer_profile import CustomerProfile

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")