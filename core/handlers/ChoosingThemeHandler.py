from .BaseHandler import BaseHandler
from models import User, AnswerToUser, UserState
from Utils import GigaChatService, choose_theme_prompt
from repository import UserSessionREPO, ThemeREPO, UserREPO


class ChoosingThemeHandler(BaseHandler):
    async def handle(self, user: User) -> AnswerToUser:
        """
        Метод для обработки состояния "choosing_theme" пользователя
        """
        themes = list(map(lambda t: t.name, await ThemeREPO.find_all()))
        prompt = choose_theme_prompt.format(
            user_text=user.payload.message.original_text,
            themes=themes
        )
        giga_answer = await GigaChatService.evaluate("Возвращай ответ в виде строки со словарем.", prompt)
        theme = giga_answer.get("theme", "")
        
        if theme in themes:
            db_session = await UserSessionREPO.get_last_session(user.uuid.userId)
            await UserSessionREPO.update({"id":db_session.id},{"theme_id":(await ThemeREPO.find_one_or_none(name=theme)).id})

            text = f"Вы выбрали тему '{theme}'. Готов начать викторину?"
            return self.make_answer(user, [text], next_state=UserState.ASKED_QUESTION.value)
        else:
            # untested
            """ если нет темы изначально """
            db_session = await UserSessionREPO.get_last_session(user.uuid.userId)
            db_user = await UserREPO.find_one_or_none(id=user.uuid.userId, first_name=db_session.user_first_name)
            themes = list(map(lambda t: t.name, await ThemeREPO.find_all()))
            text = f"{db_user.first_name}, выбери, пожалуйста, тематику викторины: {', '.join(themes)}"
            return self.make_answer(user, [text], next_state=UserState.CHOOSING_THEME.value)
        return