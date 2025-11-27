from enum import Enum
from .user_model import User
from typing import Dict

class UserState(Enum):
    CHOOSING_OPTION = "choosing_option"
    CHOOSING_THEME = "choosing_theme"
    ANALYTICS = "analytics"
    ASKED_QUESTION = "asked_question"
    ANSWERING = "answering"
    ANSWER_ANALYSIS = "answer_analysis"
    EXPLAINING = "explaining"
    DONE_QUIZ = "done_quiz"
    HELLO_USER = "hello"


class StateManager:
    def __init__(self):
        self._user_states: Dict[str, UserState] = {}


    def set_user_state(self, user: User, state: UserState) -> None:
        self._user_states[user.sessionId] = state
    
    def get_user_state(self, user: User) -> UserState:
        return self._user_states.get(user.sessionId)
    


