from abc import ABC, abstractmethod
from typing import Optional, Dict, List
import random

from models import User, AnswerToUser, Payload, Item, Bubble, Suggestions, SuggestionButton, Question
from core import StateManager
from repository import QuestionREPO


class BaseHandler(ABC):
    @abstractmethod
    async def handle(self, user: User) -> AnswerToUser:
        """
        Метод для обработки входящего запроса
        """

    def make_answer(self, user: User, text: List[str], next_state: Optional[str] = None) -> AnswerToUser:
        """
        Унифицированный способ собрать ответ пользователю с нужными полями.
        """
        payload = Payload(
            pronounceText=str(text),
            items=[Item(bubble=Bubble(text=text)) for text in text],

        )

        return AnswerToUser(
            sessionId=user.sessionId,
            messageId=user.messageId,
            uuid=user.uuid,
            payload=payload,
            next_state=next_state
        )

    def log_transition(self, user: User, from_state: str, to_state: Optional[str]) -> None:
        """
        Вспомогательный метод для логирования переходов состояний.
        """
        print(f"[Handler] {user.user_id}: {from_state} --> {to_state or 'no change'}")