import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from main.client.kafka.consumer import kafka_consumer
from main.client.kafka.default_listener import default_listener
from main.router.user_router import user_router
from main.server.kafka.producer import kafka_producer


@asynccontextmanager
async def lifespan(_: FastAPI):

    producer = kafka_producer()
    consumer = kafka_consumer()
    listeners = []
    # Запуск producer
    await producer.start()

    # Запуск consumer
    for alias, c in consumer.items():
        await c.start()

    # Запуск listener task
    listeners.append(asyncio.create_task(
        default_listener("default", consumer.get("default"))
    ))

    try:
        yield


    finally:
        await producer.stop()

        for listener in listeners:
            listener.cancel()

        for alias, c in consumer.items():
            await c.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/user", tags=["user"])
