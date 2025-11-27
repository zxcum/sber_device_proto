from .baseRepo import BaseREPO
from sqlalchemy import select, insert, values, delete, desc
from models import AgeGroup
from .database import async_session


class AgeGroupREPO(BaseREPO):
    model = AgeGroup