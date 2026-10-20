from fastapi import FastAPI
from app.redis.client import RedisClient
from app.core.config import get_settings


redis_client : RedisClient

settings = get_settings()

async def lifespan(app : FastAPI):

    redis_client = RedisClient(redis_url = settings.redis_url, cache_ttl = settings.cache_ttl, task_ttl = settings.task_ttl)
      
    yield 

    await redis_client.close()
    

#engine - движок, который отправляет сырые sql запросы в бд
# Base.metadata сохраняет всю информацию о таблицах 
# create_all создает все эти таблицы в бд       

app = FastAPI(lifespan = lifespan)

async def get_redis() -> RedisClient:

    return redis_client


