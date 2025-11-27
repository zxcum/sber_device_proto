from pydantic import BaseModel
from typing import Dict, Any
import json
from enum import Enum
from typing import Dict


class UUIDInfo(BaseModel):
    userChannel: str
    sub: str
    userId: str


class AppInfo(BaseModel):
    projectId: str
    applicationId: str
    appversionId: str
    # frontendEndpoint: str
    frontendType: str
    systemName: str
    # frontendStateId: str


class MessageContent(BaseModel):
    original_text: str
    normalized_text: str
    # asr_normalized_message: str
    entities: Dict[str, Any]
    tokenized_elements_list: list


class Payload(BaseModel):
    app_info: AppInfo
    message: MessageContent


class User(BaseModel):

    age: int = None
    name: str = None
    
    sessionId: str
    messageId: int
    uuid: UUIDInfo
    messageName: str
    payload: Payload
    

class UserState(Enum):
    CHOOSING_OPTION = "choosing_option"
    SETTING_NAME = "setting_name"
    SETTING_AGE = "setting_age"
    QUIZ_STARTING = "quiz_starting"
    CHOOSING_THEME = "choosing_theme"
    ANALYTICS = "analytics"
    ASKED_QUESTION = "asked_question"
    ANSWERING = "answering"
    ANSWER_ANALYSIS = "answer_analysis"
    EXPLAINING = "explaining"
    DONE_QUIZ = "done_quiz"
    HELLO_USER = "hello"
