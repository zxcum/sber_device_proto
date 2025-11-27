from models import User, UserState
from typing import Dict


class StateManager:
    def __init__(self):
        self._user_states: Dict[str, UserState] = {}

    def set_user_state(self, user: User, state: UserState) -> None:
        self._user_states[user.sessionId] = state
    
    def get_user_state(self, user: User) -> UserState:
        return self._user_states.get(user.sessionId)