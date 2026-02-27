"""
Service layer for conversation persistence.
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Conversation, Message


class ConversationService:
    VALID_ROLES = {"user", "assistant"}

    @staticmethod
    def create_conversation(db: Session, title: str = "New conversation") -> Conversation:
        conversation = Conversation(title=title)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation(db: Session, conversation_id: str) -> Optional[Conversation]:
        stmt = (
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .options(selectinload(Conversation.messages))
        )
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def list_conversations(db: Session, limit: int = 20) -> List[Conversation]:
        stmt = (
            select(Conversation)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def add_message(db: Session, conversation: Conversation, role: str, content: str) -> Message:
        if role not in ConversationService.VALID_ROLES:
            raise ValueError(f"Invalid role '{role}'. Expected one of: {sorted(ConversationService.VALID_ROLES)}")

        message = Message(
            conversation_id=conversation.id,
            role=role,
            content=content,
        )
        db.add(message)

        # Auto-title from first user message if still default.
        if role == "user" and conversation.title == "New conversation":
            stripped = content.strip().replace("\n", " ")
            conversation.title = stripped[:80] if len(stripped) <= 80 else f"{stripped[:77]}..."

        db.commit()
        db.refresh(message)
        db.refresh(conversation)
        return message

