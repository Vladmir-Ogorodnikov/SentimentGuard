from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.database_url, echo = True)

AsyncSessionLocal = async_sessionmaker(autocommit = False, autoflush = False, bind = engine)


async def get_db():
    db = await AsyncSessionLocal()

    try:
        yield db

     
    finally:
        await db.close()