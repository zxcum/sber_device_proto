from .BaseHandler import BaseHandler
from models import User, AnswerToUser, UserState


class HelloHandler(BaseHandler):
    async def handle(self, user: User) -> AnswerToUser:
        """
        Метод для обработки состояния "None" пользователя
        """
         
        text="Привет! Тебя приветствует викторина для детей!"
        text_2 = "Давай познакомимся! Как тебя зовут?"
        return self.make_answer(user, [text, text_2], next_state=UserState.SETTING_NAME.value)
    