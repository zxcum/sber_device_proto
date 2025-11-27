from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from .user import UUIDInfo

class SuggestionButton(BaseModel):
    title: str


class Suggestions(BaseModel):
    buttons: List[SuggestionButton]


class Bubble(BaseModel):
    text: str


class Item(BaseModel):
    bubble: Bubble


class Payload(BaseModel):
    pronounceText: str
    items: List[Item]
    # suggestions: Suggestions


class AnswerToUser(BaseModel):
    messageName: str = "ANSWER_TO_USER"
    sessionId: str
    messageId: int
    uuid: UUIDInfo
    payload: Payload

    next_state: Optional[str] = Field(default=None, exclude=True)