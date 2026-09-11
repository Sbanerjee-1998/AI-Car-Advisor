from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.app.models import Conversation, Message, User
from backend.app.schemas.errors import AppError


def owned_conversation(db: Session, conversation_id: int, user_id: int) -> Conversation:
    conversation = db.scalar(
        select(Conversation).options(selectinload(Conversation.messages), selectinload(Conversation.preference)).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
    )
    if conversation is None:
        raise AppError(404, "not_found", "Conversation was not found.")
    return conversation


def create_conversation(db: Session, user: User, title: str | None = None) -> Conversation:
    conversation = Conversation(user_id=user.id, title=(title or None))
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def list_conversations(db: Session, user_id: int) -> list[Conversation]:
    return list(db.scalars(select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())))


def delete_conversation(db: Session, conversation: Conversation) -> None:
    db.delete(conversation)
    db.commit()


def add_message(db: Session, conversation: Conversation, role: str, content: str) -> Message:
    message = Message(conversation_id=conversation.id, role=role, content=content)
    db.add(message)
    db.flush()
    return message
