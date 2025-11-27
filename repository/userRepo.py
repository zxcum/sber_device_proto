from .baseRepo import BaseREPO
from sqlalchemy import select, insert, values, delete, desc
from models import Theme, Answer, UserDB, UserSession, Question
from .database import async_session


class UserREPO(BaseREPO):
    model = UserDB

    @classmethod
    async def get_user_form(cls, username: str, session: str) -> dict:
        """
        Для получения последних записей пользователя из БД (Вопрос, ответ, тема) в метод необходимо передать 
        username пользователя и значение session равное номеру последней сессии
        """
        async with async_session() as sess:
            query = (
                select(UserDB, UserSession, Answer, Question, Theme)
                .join(UserSession, UserDB.id == UserSession.user_id)
                .join(Answer, UserSession.id == Answer.session_id)
                .join(Question, Answer.question_id == Question.id)
                .join(Theme, Question.theme_id == Theme.id)
                .filter(Answer.session_id == session)
            )
            result = await sess.execute(query)

            rows = result.all()

            parsed_data = []
            for user, session, answer, main_question, theme in rows:
                data = {
                    'user_id': user.id,
                    'first_name': user.first_name,
                    'answer_text': answer.text,
                    'answer_date': answer.date.isoformat() if answer.date else None,
                    'question_text': main_question.text,
                    'theme_text': theme.text,
                }
                parsed_data.append(data)

            return parsed_data


    @classmethod
    async def add(cls, **kwargs):
        async with async_session() as sess:
            query = select(cls.model).filter_by(**kwargs)
            user = (await sess.execute(query)).one_or_none()
            if not user:
                query = insert(cls.model).values(**kwargs)
                await sess.execute(query)
                await sess.commit()