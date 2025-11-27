from pydantic import BaseModel
from typing import Dict, Any
import json
from enum import Enum
from typing import Dict


class Question(BaseModel):
    number: int
    question: str
    answer: str
    fact: str
    hint: str