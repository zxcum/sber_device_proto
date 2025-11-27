from .baseRepo import BaseREPO
from models import Answer, User
from .database import async_session
from sqlalchemy import select, insert, values, delete
from sqlalchemy import func


class AnswerREPO(BaseREPO):
    model = Answer

    @classmethod
    async def get_last_session(cls, chat_id: int):
        async with async_session() as sess:
            query = select(User).filter_by(chat_id=chat_id)
            user_id = ((await sess.execute(query)).scalar()).id
            max_session = await sess.query(func.max(cls.model.session)).filter(
                cls.model.user_id == user_id).scalar()
            
            if max_session:
                return int(max_session)
            else:
                return 1