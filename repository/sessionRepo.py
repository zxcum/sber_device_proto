from .baseRepo import BaseREPO
from models import UserSession, User
from .database import async_session
from sqlalchemy import select, insert, values, delete


class UserSessionREPO(BaseREPO):
    model = UserSession

    @classmethod
    async def create_new_session(cls, chat_id):
        async with async_session() as sess:
            query_user = select(User).filter_by(chat_id=chat_id)
            user = (await sess.execute(query_user)).scalar()
            if user:
                query_session = insert(cls.model).values(
                    user_id=user.id).returning(cls.model.id)
                result = (await sess.execute(query_session)).scalar()
                await sess.commit()

                return result
            return None

    @classmethod
    async def get_last_session(cls, userId):
        async with async_session() as sess:
            query_session = select(cls.model).filter_by(
                user_id=userId).order_by(cls.model.started_at.desc()).limit(1)
            result = (await sess.execute(query_session)).scalar()
            return result
