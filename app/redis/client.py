import redis.asyncio as redis
import json
from typing import Optional


class RedisClient:

    def __init__(self, redis_url : str, cache_ttl : Optional[int] = None, task_ttl : Optional[int] = None):

        self.redis = redis.Redis.from_url(redis_url, decode_responses = True)
        self.cache_ttl = cache_ttl
        self.task_ttl = task_ttl

    async def close(self) -> None:

        if self.redis:
            await self.redis.aclose()     

    async def get_cache(self, text_hash: str) -> Optional[dict]:

        key = f"prediction:{text_hash}"

        result = await self.redis.get(key)

        if result:

            return json.loads(result)
        return None 
    
    async def set_cache(self, text_hash : str, data : dict) -> None:

        key = f"prediction:{text_hash}"

        await self.redis.set(key, json.dumps(data), ex = self.cache_ttl)

    async def get_task(self, task_id : str) -> Optional[dict]:

       key = f"task:{task_id}"

       result = await self.redis.get(key)

       if result:
           return json.loads(result)
       return None   

    async def set_task(self, task_id : str, data : dict) -> None:

        key = f"task:{task_id}"

        await self.redis.set(key, json.dumps(data), ex = self.task_ttl) 






     