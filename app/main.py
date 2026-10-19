from fastapi import FastAPI
from app.models.base import Base
from app.db.session import engine


async def lifespan(app : FastAPI):

    await Base.metadata.create_all(bind = engine)
    yield 
    print("Соединение закрыто")

#engine - движок, который отправляет сырые sql запросы в бд
# Base.metadata сохраняет всю информацию о таблицах 
# create_all создает все эти таблицы в бд       


app = FastAPI(lifespan = lifespan)




