from .StateManager import StateManager
from models import User, UserState, AnswerToUser
from typing import Dict
from .handlers import BaseHandler


class AppRouter:
    """
    Класс, предназначенный для вызова хэндлера по состоянию пользователя
    """

    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.handlers: Dict[UserState] = {}



    def register_handler(self, state_name: str, handler: BaseHandler):
        """
        Добавление новых хэндлеров
        """
        self.handlers[state_name] = handler
        return self

    async def route(self, user: User) -> AnswerToUser:
        """
        Основной метод для вызова нужного хэндлера и изменения состояния пользователя
        """

        print(self.state_manager._user_states)

        state = self.state_manager.get_user_state(user)
        handler = self.handlers.get(state)

        # получение ответа для пользователя
        if state in [UserState.SETTING_AGE.value, UserState.SETTING_NAME.value, UserState.ASKED_QUESTION.value]:
            print("state with stateManager")
            answer = await handler.handle(user, self.state_manager)
        else:
            answer = await handler.handle(user)
        
        
        if not answer:
            text = "Не расслышал, повтори еще раз"
            return handler.make_answer(user, [text])
        # изменение состояния пользователя
        print(answer.next_state)
        self.state_manager.set_user_state(user, answer.next_state)

        return answer
