import json
from datetime import datetime

from .BaseHandler import BaseHandler
from models import User, AnswerToUser, UserState, Answer
from Utils import GigaChatService, question_verify_prompt, yes_no_prompt
from core import StateManager
from repository import QuestionREPO, UserSessionREPO, AnswerREPO, UserREPO


class QuestionHandler(BaseHandler):
    async def handle(self, user: User, stateManager: StateManager) -> AnswerToUser:
        """
        Метод для обработки состояния "asked_question" пользователя
        """
        # Запрос в БД - проверка на количество заданных вопросов
        db_session = await UserSessionREPO.get_last_session(user.uuid.userId)
        answers = await AnswerREPO.find_all(session_id=db_session.id, text=None)
        if len(answers) == 0:
            prompt = yes_no_prompt.format(
                user_text=user.payload.message.original_text,
            )
            giga_answer = await GigaChatService.evaluate("Возвращай ответ в виде строки со словарем.", prompt)

        # Проверка пользователя на готовность к ответам на вопросы
            if giga_answer["response"]:
                # Создание списка вопросов для сессии
                await QuestionREPO.set_random_question_to_user(userId=user.uuid.userId)

                next_question_id = (await AnswerREPO.find_one_or_none(session_id=db_session.id, text=None)).question_id
                question_text = (await QuestionREPO.find_by_id(next_question_id)).text

                return self.make_answer(user, [question_text], next_state=UserState.ASKED_QUESTION.value)
            else:
                return
            
        # Получение вопроса, на который пользователь уже дал ответ
        last_question_id = (await AnswerREPO.find_one_or_none(session_id=db_session.id, text=None)).question_id
        last_question = await QuestionREPO.find_by_id(last_question_id)

        # Обращение к Гигачату на правильность ответа пользователя
        prompt = question_verify_prompt.format(
            user_text=user.payload.message.original_text,
            question_text=last_question.text,
            right_answer=last_question.right_answer
        )
        giga_answer = await GigaChatService.evaluate("Возвращай ответ в виде строки со словарем.", prompt)


        if giga_answer["response"]:
            # Добавление ответа пользователя в БД
            await AnswerREPO.update({"session_id": db_session.id, "question_id": last_question_id}, {"text": user.payload.message.original_text})

            # Проверка на все отвеченные вопросы
            answers = await AnswerREPO.find_all(session_id=db_session.id, filters=[Answer.text != None])
            if len(answers) == 5:
                msg_1 = f"Молодец! Интересный факт:{last_question.fact}"
                msg_2 = "Викторина пройдена!Ты хочешь пройти викторину еще раз или посмотреть аналитику? "
                return self.make_answer(user, [msg_1, msg_2], next_state=None)

            # Создание нового вопроса
            await QuestionREPO.set_random_question_to_user(userId=user.uuid.userId)
            next_question_id = (await AnswerREPO.find_one_or_none(session_id=db_session.id, text=None)).question_id
            question_text = (await QuestionREPO.find_by_id(next_question_id)).text

            msg_1 = f"Молодец! Интересный факт:{last_question.fact}"
            msg_2 = f"Следующий вопрос: {question_text}"
            return self.make_answer(user, [msg_1, msg_2], next_state=UserState.ASKED_QUESTION.value)

        msg_1 = f"Попробуй еще раз. Твой вопрос:{last_question.text}."
        msg_2 = f"Вот подсказка:{last_question.hint}"
        return self.make_answer(user, [msg_1, msg_2], next_state=UserState.ASKED_QUESTION.value)
