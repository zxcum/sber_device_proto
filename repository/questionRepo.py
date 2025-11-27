from datetime import datetime
from sqlalchemy import select, insert, values, delete, func
from models import Question, Answer
from .baseRepo import BaseREPO
from .database import async_session
from .sessionRepo import UserSessionREPO
from .userRepo import UserREPO
from .ageGroupRepo import AgeGroupREPO
from .answerRepo import AnswerREPO


class QuestionREPO(BaseREPO):
    model = Question

    @classmethod
    async def set_random_question_to_user(cls, userId: str):
        async with async_session() as sess:
            db_session = await UserSessionREPO.get_last_session(userId)
            user = await UserREPO.find_one_or_none(id=db_session.user_id, first_name=db_session.user_first_name)
            
            age_groups = await AgeGroupREPO.find_all()
            current_age_group_id = age_groups[-1].id
            user_age = datetime.now().year - int(user.year_of_birth)

            for group in age_groups:
                if user_age >= group.age_from and user_age <= group.age_to:
                    current_age_group_id = group.id
            
            random_question_query = (
                select(cls.model)
                .filter_by(theme_id=db_session.theme_id, age_group_id=current_age_group_id)
                .order_by(func.random())
                .limit(1)
            )

            random_question = (await sess.execute(random_question_query)).scalar()
            current_questions_id = list(map(lambda a: a.question_id, await AnswerREPO.find_all(session_id=db_session.id)))
            
            # Обработка случая, когда вопрос случайным образом повторился
            while random_question.id in current_questions_id:
                random_question = (await sess.execute(random_question_query)).scalar()

            await AnswerREPO.add(question_id=random_question.id, session_id=db_session.id)

            
        

