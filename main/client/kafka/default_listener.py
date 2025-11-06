import asyncio
import logging as log

from aiokafka import AIOKafkaConsumer


async def default_listener(alias: str, consumer: AIOKafkaConsumer):
    """
    Default kafka listener для топика с alias

    Args:
        alias (str): алиас топика который необходимо слушать
        consumer (AIOKafkaConsumer): интанс консьюмера
    """
    try:
        async for msg in consumer:
            log.info(f"Получено сообщение для {alias} topic {msg.topic}:: {msg.key} : {msg.value}")
    except asyncio.CancelledError:
        # graceful shutdown
        log.error("Ошибка при получении сообщения")
        raise
