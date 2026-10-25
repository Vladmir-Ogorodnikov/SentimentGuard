from fastapi import FastAPI
from app.redis.client import redis_client
from app.core.config import settings
from rabbit import rabbit_client 
from app.routers.predictions import prediction_router





async def lifespan(app : FastAPI):
    print(f"🔍 DEBUG: settings.redis_url = '{getattr(settings, 'redis_url', 'НЕ НАЙДЕНО')}'")
    print(f"🔍 DEBUG: Все настройки: {settings.model_dump() if hasattr(settings, 'model_dump') else settings.__dict__}")  
    
    await redis_client.redis.ping()
    print("Redis подключен")

      
    await rabbit_client.connect()
    print("Rabbit подключен")

      
    yield 

    await redis_client.close()
    print("Raddis отключен")
    await rabbit_client.close()
    print("Rabbit отключен")


    

app = FastAPI(lifespan = lifespan)

app.include_router(prediction_router)


