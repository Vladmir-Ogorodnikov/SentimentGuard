import aio_pika
import json  
from app.core.config import get_settings

settings = get_settings()

class RabbitMQ:

    def __init__(self):

        self.connection : aio_pika.RobustConnection = None
        self.channel : aio_pika.Channel = None 
        self.exchange : aio_pika.Exchange = None 


    async def connect(self) -> None:

        self.connection = await aio_pika.connect_robust(settings.rabbit_url)

        self.channel = await self.connection.channel()       

        self.exchange = await self.channel.declare_exchange(
            name = settings.rabbit_exchange,
            type = aio_pika.ExchangeType.DIRECT,
            durable = True
        )

        queue_new = await self.channel.declare_queue(
            name = settings.rabbit_queue_new,
            durable = True
        )

        queue_done = await self.channel.declare_queue(
            name = settings.rabbit_queue_done,
            durable = True
        )

        await queue_new.bind(self.exchange, routing_key = settings.rabbit_routing_key_new)
        await queue_done.bind(self.exchange, routing_key = settings.rabbit_routing_key_done)

        
    
    async def close(self) -> None:

        if self.connection:
            await self.connection.close()
         

    async def publish_to_classify(self, message_data: dict) -> None:

        try:

            message = aio_pika.Message(
                body = json.dumps(message_data).encode(),
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT

            )    

            await self.exchange.publish(message, routing_key = settings.rabbit_routing_key_new) 

            
        except Exception:
            raise 

    async def publish_to_done(self, message_data: dict) -> None:

        try:

            message = aio_pika.Message(
                body = json.dumps(message_data).encode(),
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT

            )    

            await self.exchange.publish(message, routing_key = settings.rabbit_routing_key_done) 

            
        except Exception:
            raise 


        
rabbit_client = RabbitMQ()

async def get_rabbit() -> RabbitMQ:

    return rabbit_client 
 
             
