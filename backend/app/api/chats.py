from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from backend.app.agents.advisor import AdvisorService
from backend.app.api.dependencies import get_current_user, get_db
from backend.app.models import User
from backend.app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationCreate,
    ConversationDetail,
    ConversationSummary,
    MessageResponse,
    PreferenceResponse,
)
from backend.app.schemas.errors import AppError
from backend.app.services.chat import add_message, create_conversation, delete_conversation, list_conversations, owned_conversation
from backend.app.services.preferences import preference_dict

router = APIRouter(prefix="/api/chats", tags=["chats"])


def _summary(conversation):
    return ConversationSummary.model_validate(conversation)


def _detail(conversation):
    return ConversationDetail(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[MessageResponse.model_validate(message) for message in sorted(conversation.messages, key=lambda item: item.created_at)],
        preferences=PreferenceResponse(**preference_dict(conversation.preference)) if conversation.preference else None,
    )


@router.get("", response_model=dict)
def get_chats(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"items": [_summary(item) for item in list_conversations(db, user.id)]}


@router.post("", response_model=ConversationSummary, status_code=201)
def new_chat(payload: ConversationCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_conversation(db, user, payload.title)


@router.get("/{chat_id}", response_model=ConversationDetail)
def get_chat(chat_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _detail(owned_conversation(db, chat_id, user.id))


@router.delete("/{chat_id}", status_code=204)
def remove_chat(chat_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    delete_conversation(db, owned_conversation(db, chat_id, user.id))


@router.post("/{chat_id}/messages", response_model=ChatMessageResponse)
def send_message(chat_id: int, payload: ChatMessageRequest, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    content = payload.content.strip()
    if not content:
        raise AppError(422, "validation_error", "Please enter a message.", {"content": "Message cannot be blank."})
    if len(content) > request.app.state.settings.max_message_length:
        raise AppError(422, "validation_error", "Please shorten your message.", {"content": "Message is too long."})
    conversation = owned_conversation(db, chat_id, user.id)
    user_message = add_message(db, conversation, "user", content)
    result = request.app.state.advisor.respond(db, conversation, content)
    assistant_message = add_message(db, conversation, "assistant", result.content)
    if conversation.title is None:
        conversation.title = " ".join(content.split()[:8])[:160]
    conversation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user_message)
    db.refresh(assistant_message)
    return ChatMessageResponse(
        conversation_id=conversation.id,
        user_message=MessageResponse.model_validate(user_message),
        assistant_message=MessageResponse.model_validate(assistant_message),
        recommendations=result.recommendations,
        follow_up_required=result.follow_up_required,
        available_actions=result.available_actions,
        disclaimer="Prices and specifications are approximate and should be verified with an authorized dealer.",
    )
