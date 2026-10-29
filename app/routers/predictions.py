from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.prediction import PredictionRequest, PredictionResponse, TaskResponse, PredictionResult, HealthResponse  
from app.redis.client import RedisClient, get_redis
from rabbit import RabbitMQ, get_rabbit
import hashlib
from uuid import uuid4, UUID
from datetime import datetime, timezone



def create_hash(data : str) -> str:
    hash_object = hashlib.sha256(data.encode())
    return hash_object.hexdigest()



prediction_router = APIRouter(prefix = "/api/v1", tags = ["predictions"])

@prediction_router.post("/predict", status_code = status.HTTP_202_ACCEPTED)
async def predict(request : PredictionRequest,
                   redis : RedisClient = Depends(get_redis),
                   rabbit : RabbitMQ = Depends(get_rabbit)) -> PredictionResponse: 

    text_hash = create_hash(data = request.text)

    redis_result = await redis.get_cache(text_hash) 

    if redis_result:

        return PredictionResponse(
            task_id = uuid4(),
            status = "done",
            cached = True,
            sentiment = redis_result.get("sentiment"),
            confidence=redis_result.get("confidence"),
            is_toxic=redis_result.get("is_toxic"),
            created_at=redis_result.get("created_at")
        )
    

    task_id = uuid4()
    redis_task = {
        "task_id" : str(task_id),
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": None,
        "sentiment": None,
        "confidence": None,
        "is_toxic": None 
    }
    
    await redis.set_task(task_id = str(task_id), data = redis_task)

    message = {
        "task_id": str(task_id),
        "text": request.text,
        "text_hash": text_hash,
        "created_at": redis_task["created_at"]
    }

    redis_task["status"] = "processing"
    await redis.set_task(str(task_id), redis_task)

    # Только потом отправляем в очередь
    try:
        await rabbit.publish_to_classify(message)
    except Exception as e:
        redis_task["status"] = "failed"
        redis_task["error_message"] = str(e)
        await redis.set_task(str(task_id), redis_task)
        raise HTTPException(status_code=500, detail="Failed to queue prediction task")

    return PredictionResponse(
        task_id=task_id,
        status="processing",
        cached=False
    )
 
@prediction_router.get("/tasks/{task_id}", status_code = status.HTTP_200_OK)
async def get_task(task_id : UUID, redis : RedisClient = Depends(get_redis)) -> TaskResponse:

    result = await redis.get_task(str(task_id))

    if not result:

        raise HTTPException(status_code = 404, detail = "Task not found")
    
    return TaskResponse(**result)
                        

@prediction_router.get("/predict/fast", status_code = status.HTTP_200_OK)
async def fast_predict(text : str, redis : RedisClient = Depends(get_redis)) -> PredictionResult:

    if len(text) < 5:
        raise HTTPException(status_code=422, detail="Text must be at least 5 characters")
    
    text_hash = create_hash(data = text)
    result = await redis.get_cache(text_hash = text_hash)

    if not result:
        raise HTTPException(status_code=404, detail="Prediction not found in cache")
    
    return PredictionResult(**result)


@prediction_router.get("/health", status_code = status.HTTP_200_OK, tags = ["health"])
async def get_health(redis : RedisClient = Depends(get_redis), rabbit : RabbitMQ = Depends(get_rabbit)) -> HealthResponse:
    
    try:
        await redis.redis.ping()
        redis_connect = True
    except Exception:
        redis_connect = False 

    rabbit_connect = rabbit.connection is not None and not rabbit.connection.is_closed

    health_status = "ok" if redis_connect and rabbit_connect else "degraded"

    return HealthResponse(
        status = health_status,
        redis = redis_connect,
        rabbit = rabbit_connect
    )


