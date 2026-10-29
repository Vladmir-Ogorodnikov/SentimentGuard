import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import json
import aio_pika
from app.redis.client import RedisClient
from rabbit import RabbitMQ
from app.core.config import settings
from ml_worker.model import MockSentimentModel
from ml_worker.publisher import ResultPublisher




model = MockSentimentModel()

publisher = None 

async def process_message(message : aio_pika.IncomingMessage) -> None:

    async with message.process():

        body = json.loads(message.body)
        task_id = body["task_id"]
        text = body["text"]
        text_hash = body["text_hash"]
        
        print(f"Получена задача {task_id}")
        
        try:
            prediction = model.predict(text)
            await publisher.publish_result(task_id, text_hash, prediction, error_message=None)
            print(f"Задача {task_id} обработана успешно")
        except Exception as e:
            error_msg = str(e)
            print(f"Ошибка при обработке задачи {task_id}: {error_msg}")
            await publisher.publish_result(task_id, text_hash, {}, error_message=error_msg)

        


async def main() -> None:

    redis_client = RedisClient(redis_url = settings.redis_url, 
                               cache_ttl = settings.cache_ttl, 
                               task_ttl = settings.task_ttl)
    
    rabbit_client = RabbitMQ()

    await rabbit_client.connect()

    global publisher

    publisher = ResultPublisher(redis_client, rabbit_client)

    channel = await rabbit_client.connection.channel()
    await channel.set_qos(prefetch_count=1)
    
    queue = await channel.declare_queue(settings.rabbit_queue_new, durable=True)
    await queue.consume(process_message)


    try:
        await asyncio.Future()  # Бесконечное ожидание
    except KeyboardInterrupt:
        print("\nОстановка ML Worker...")
    finally:
        await rabbit_client.close()
        print("RabbitMQ отключен")


    
if __name__ == "__main__":

    asyncio.run(main())



