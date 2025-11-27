from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from Utils import DB_HOST, DB_PASS, DB_NAME, DB_USER, DB_PORT


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# DATABASE_URL = "sqlite+aiosqlite:///sqlite.db"
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)