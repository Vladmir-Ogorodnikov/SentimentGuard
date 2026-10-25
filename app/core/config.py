from dataclasses import dataclass 
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:

    redis_url : str 
    cache_ttl : int  
    task_ttl : int
    rabbit_url : str
    rabbit_exchange : str
    rabbit_queue_new : str
    rabbit_queue_done : str
    rabbit_routing_key_new : str
    rabbit_routing_key_done : str
    

def get_settings() -> Settings:

    return Settings(
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        cache_ttl=int(os.getenv("CACHE_TTL", "86400")),
        task_ttl=int(os.getenv("TASK_TTL", "3600")),
        rabbit_url=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/"),
        rabbit_exchange=os.getenv("RABBIT_EXCHANGE", "predictions"),
        rabbit_queue_new=os.getenv("RABBIT_QUEUE_NEW", "predictions.new"),
        rabbit_queue_done=os.getenv("RABBIT_QUEUE_DONE", "predictions.done"),
        rabbit_routing_key_new=os.getenv("RABBIT_ROUTING_KEY_NEW", "prediction.new"),
        rabbit_routing_key_done=os.getenv("RABBIT_ROUTING_KEY_DONE", "prediction.done")



    )

settings = get_settings()