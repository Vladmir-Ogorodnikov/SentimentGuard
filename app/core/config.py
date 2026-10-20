from dataclasses import dataclass 
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:

    redis_url : str 
    cache_ttl : int  
    task_ttl : int

def get_settings() -> Settings:

    return Settings(
        redis_url = os.getenv("REDIS_URL"),
        cache_ttl = os.getenv("CACHE_TTL"),
        task_ttl = os.getenv("TASK_TTL")
    )