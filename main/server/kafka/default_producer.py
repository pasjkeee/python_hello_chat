import logging as log
from typing import Annotated

from fastapi import Depends

from main.config.settings import get_settings
from main.model.kafka.user_created_msg import UserCreatedMsg
from main.server.kafka.producer import KafkaProducerDepends


class DefaultProducer:
    """
    Продьюсер для топика с alias "default"
    """

    def __init__(self, producer: KafkaProducerDepends):
        self.producer = producer

    async def send_user_created_msg(self, key: str, value: UserCreatedMsg):
        log.info(f"Отправка сообщения о создании пользователя с id {key}")
        await self.producer.send(get_settings().kafka.producer.topics.default, key=key, value=value)


DefaultProducerDepends = Annotated[DefaultProducer, Depends()]