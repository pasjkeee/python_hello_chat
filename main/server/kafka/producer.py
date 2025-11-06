
from functools import lru_cache
from typing import Annotated

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from main.config.kafka import ProducerKafkaSettings
from main.config.settings import get_settings


@lru_cache
def kafka_producer() -> AIOKafkaProducer:
    """
    Создаёт Kafka-консьюмера на основе конфигурации.
    """
    settings: ProducerKafkaSettings = get_settings().kafka.producer
    return AIOKafkaProducer(
        bootstrap_servers=settings.bootstrap_servers,
        client_id=settings.client_id,
        acks=settings.acks,
        key_serializer=settings.key_serializer,
        value_serializer=settings.value_serializer)


KafkaProducerDepends = Annotated[AIOKafkaProducer, Depends(kafka_producer)]
