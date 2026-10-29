from app.redis.client import RedisClient
from rabbit import RabbitMQ
from datetime import datetime, timezone

class ResultPublisher:

    def __init__(self, redis_client : RedisClient, rabbit : RabbitMQ) -> None:
        self.redis_client = redis_client
        self.rabbit = rabbit 

    async def publish_result(self, task_id: str, text_hash: str,
                            prediction: dict, error_message: str = None):
        processed_at = datetime.now(timezone.utc).isoformat()

        

        
        task_data = {
            "task_id": task_id,
            "status": "done" if not error_message else "failed",
            "sentiment": prediction.get("sentiment"),
            "confidence": prediction.get("confidence"),
            "is_toxic": prediction.get("is_toxic"),
            "error_message": error_message,
            "completed_at": processed_at
        }

        await self.redis_client.set_task(task_id, task_data)

        if not error_message: 

            cache_data = {
                    "sentiment": prediction["sentiment"],
                    "confidence": prediction["confidence"],
                    "is_toxic": prediction["is_toxic"],
                    "created_at": processed_at
                }
            await self.redis_client.set_cache(text_hash, cache_data)

        message = {
                "task_id": task_id,
                "text_hash": text_hash,
                "status": "success" if not error_message else "error",
                "sentiment": prediction.get("sentiment"),
                "confidence": prediction.get("confidence"),
                "is_toxic": prediction.get("is_toxic"),
                "error_message": error_message,
                "processed_at": processed_at
            }

        await self.rabbit.publish_to_done(message) 

          



