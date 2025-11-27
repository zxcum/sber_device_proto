from .database import async_session
from sqlalchemy import select, insert, values, delete, update


class BaseREPO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session() as sess:
            query = select(cls.model).filter_by(id=model_id)
            models = await sess.execute(query)
            return models.scalars().one_or_none()

    @classmethod
    async def find_all(cls, filters=None, **kwargs):
        async with async_session() as sess:
            query = select(cls.model).filter_by(**kwargs)
            if filters:
                query = query.filter(*filters)
            models = await sess.execute(query)
            return models.scalars().all()
    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as sess:
            query = select(cls.model).filter_by(**filter_by)
            models = await sess.execute(query)
            return models.scalar()

    @classmethod
    async def add(cls, **kwargs):
        async with async_session() as sess:
            query = insert(cls.model).values(**kwargs)
            result = await sess.execute(query)
            await sess.commit()
    
    @classmethod
    async def update(cls, filters: dict, values: dict) -> None:
        async with async_session() as sess:
            query = update(cls.model).filter_by(**filters).values(**values)
            await sess.execute(query)
            await sess.commit()
