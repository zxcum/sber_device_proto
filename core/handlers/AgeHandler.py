from datetime import datetime

from .BaseHandler import BaseHandler
from models import User, AnswerToUser, UserState
from core import StateManager
from Utils import GigaChatService, getting_age_prompt
from repository import UserREPO, UserSessionREPO, ThemeREPO


class AgeHandler(BaseHandler):
    async def handle(self, user: User, stateManager: StateManager) -> AnswerToUser:
        """
        Метод для обработки состояния "setting_age" пользователя
        """
        db_session = await UserSessionREPO.get_last_session(user.uuid.userId)
        db_user = await UserREPO.find_one_or_none(id=user.uuid.userId, first_name=db_session.user_first_name)

        # Тематики викторин из БД
        themes = list(map(lambda t: t.name, await ThemeREPO.find_all()))

        if not db_user.year_of_birth:
            prompt = getting_age_prompt.format(
                user_text=user.payload.message.original_text,
            )
            giga_answer = await GigaChatService.evaluate("Возвращай ответ в виде строки со словарем.", prompt)

            if giga_answer["response"]:

                year_of_birth = datetime.now().year - int(giga_answer["response"])
                await UserREPO.update({"id": user.uuid.userId, "first_name": db_user.first_name}, {"year_of_birth": year_of_birth})

                text = f"{db_user.first_name}, выбери, пожалуйста, тематику викторины: {', '.join(themes)}"
                return self.make_answer(user, [text], next_state=UserState.CHOOSING_THEME.value)
        else:
            text = f"{db_user.first_name}, выбери, пожалуйста, тематику викторины: {', '.join(themes)}"
            return self.make_answer(user, [text], next_state=UserState.CHOOSING_THEME.value)
        return
