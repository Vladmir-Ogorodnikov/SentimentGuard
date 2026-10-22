from fastapi import APIRouter, status, Depends
from app.schemas.prediction import PredictionRequest, PredictionResponse  
from app.redis.client import RedisClient, get_redis
from rabbit import RabbitMQ, get_rabbit

prediction_router = APIRouter(prefix = "/api/v1", tags = ["predictions"])

@prediction_router.post("/predict", status_code = status.HTTP_202_ACCEPTED)
async def predict(data : PredictionRequest,
                   redis : RedisClient = Depends(get_redis),
                   rabbit : RabbitMQ = Depends(get_rabbit)) -> PredictionResponse:  
    ...
