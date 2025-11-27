from gigachat import GigaChatAsyncClient
from .config import GIGACHAT_AUTH_BASIC, GIGACHAT_MODEL, GIGACHAT_SCOPE
from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
import json


class GigaChatService:
    _gigachat = GigaChat(
        credentials=GIGACHAT_AUTH_BASIC,
        scope=GIGACHAT_SCOPE,
        model=GIGACHAT_MODEL,
        verify_ssl_certs=False
    )

    @classmethod
    async def evaluate(cls, system_prompt: str, user_prompt: str):

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        chain = cls._gigachat | StrOutputParser()

        response = await chain.ainvoke(messages)
        try:
            giga_answer = json.loads(response)
            if "response" not in giga_answer:
                raise Exception
        except Exception:
            giga_answer = {"response": None}
        return giga_answer