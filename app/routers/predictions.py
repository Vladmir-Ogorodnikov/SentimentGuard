from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.prediction import PredictionRequest, PredictionResponse  
from app.redis.client import RedisClient, get_redis
from rabbit import RabbitMQ, get_rabbit
import hashlib
from uuid import uuid4
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

    try:
        await rabbit.publish_to_classify(message)
        
        redis_task["status"] = "processing"
        await redis.set_task(str(task_id), redis_task)
        return PredictionResponse(
            task_id = task_id,
            status = "processing",
            cached = False

        )

    except Exception as e:
        result = await redis.get_task(str(task_id))
        result["status"] = "failed"
        result["error_message"] = str(e)
        await redis.set_task(str(task_id), result)
        raise HTTPException(status_code=500, detail="Failed to queue prediction task")


    
