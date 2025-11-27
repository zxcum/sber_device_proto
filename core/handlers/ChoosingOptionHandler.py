import json

from .BaseHandler import BaseHandler
from models import User, AnswerToUser, UserState
from Utils import GigaChatService, choose_option_prompt


class ChoosingOptionHandler(BaseHandler):
    async def handle(self, user: User) -> AnswerToUser:
        """
        Метод для обработки состояния "choosing_option" пользователя
        """

        prompt = choose_option_prompt.format(
            user_text=user.payload.message.original_text)
        giga_answer = await GigaChatService.evaluate("Возвращай ответ в виде строки со словарем.", prompt)
        
        match giga_answer["response"]:
            case False:
                text = "Ваша аналитика"
                return self.make_answer(user, [text], next_state=UserState.ANALYTICS.value)
            case True:
                text = "Как тебя зовут?"
                return self.make_answer(user, [text], next_state=UserState.SETTING_NAME.value)
            case None:
                return None
