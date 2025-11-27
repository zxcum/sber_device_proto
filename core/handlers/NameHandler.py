from .BaseHandler import BaseHandler
from models import User, AnswerToUser, UserState
from core import StateManager
from Utils import GigaChatService, getting_name_prompt
from repository import UserREPO, UserSessionREPO


class NameHandler(BaseHandler):
    async def handle(self, user: User, stateManager: StateManager) -> AnswerToUser:
        """
        Метод для обработки состояния "setting_name" пользователя
        """
        # Добавление в базу данных имя пользователя
        prompt = getting_name_prompt.format(
            user_text=user.payload.message.original_text,
            )
        print(prompt)
        giga_answer = await GigaChatService.evaluate("Возвращай ответ в виде строки со словарем.", prompt)
        

        if giga_answer["response"]:
            await UserREPO.add(id=user.uuid.userId, first_name=giga_answer["response"])
            await UserSessionREPO.add(user_id=user.uuid.userId, user_first_name=giga_answer["response"])
            
            text = f"Привет, {giga_answer['response']}, приятно познакомиться, сколько тебе лет?"
            return self.make_answer(user, [text], next_state=UserState.SETTING_AGE.value)
        else:
            return self.make_answer(user, ["Не расслышал твое имя, можешь его повторить, пожалуйста"], next_state=UserState.SETTING_NAME.value)
        return
