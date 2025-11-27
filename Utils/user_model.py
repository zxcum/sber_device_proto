from pydantic import BaseModel
from typing import Dict, Any
import json

class UUIDInfo(BaseModel):
    userChannel: str
    sub: str
    userId: int


class AppInfo(BaseModel):
    projectId: str
    applicationId: str
    appversionId: str
    frontendEndpoint: str
    frontendType: str
    systemName: str
    frontendStateId: str


class MessageContent(BaseModel):
    original_text: str
    normalized_text: str
    asr_normalized_message: str
    entities: Dict[str, Any]
    tokenized_elements_list: list


class Payload(BaseModel):
    app_info: AppInfo
    message: MessageContent


class User(BaseModel):
    sessionId: str
    messageId: int
    uuid: UUIDInfo
    messageName: str
    payload: Payload


def parse_request_to_user(request_json: str) -> User:

    if isinstance(request_json, str):
        data = json.loads(request_json)
    else:
        data = request_json

    return User(**data)