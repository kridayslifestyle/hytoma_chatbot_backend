from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.database.session import get_db
from app.ai.llm_service import generate_reply
from app.services.chat_service import save_message, get_history
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.utils.constants import (
    MAX_HISTORY,
    SUMMARY_TRIGGER,
    SYSTEM_PROMPT
)
from app.services.ai_chat_service import ai_chat
from app.ai.profile_extractor import extract_profile

from app.services.profile_service import (
    update_profile
)

from app.ai.llm_service import (
    generate_reply,
    generate_summary
)

from app.services.summary_service import (
    get_summary,
    save_summary
)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(
        request: ChatRequest,
        db: Session = Depends(get_db)
):

    reply = ai_chat(
        db,
        request.customer_id,
        request.message
    )

    return ChatResponse(
        response=reply
    )