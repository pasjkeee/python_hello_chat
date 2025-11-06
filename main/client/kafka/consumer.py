from functools import lru_cache
from typing import Dict

from aiokafka import AIOKafkaConsumer

from main.config.settings import get_settings


@lru_cache
def kafka_consumer() -> Dict[str, AIOKafkaConsumer]:
    """
    Создаёт набор Kafka-консьюмеров на основе конфигурации.

    Структура KAFKA__CONSUMER__TOPICS:
        {
            "alias1": "topic_name_1",
            "alias2": "topic_name_2",
            ...
        }

    Пример результата:
        {
            "user_events": <AIOKafkaConsumer>,
            "audit_logs": <AIOKafkaConsumer>,
        }

    Returns:
        dict[str, AIOKafkaConsumer]:
            Словарь алиас -> экземпляр AIOKafkaConsumer.
            Консьюмеры на этом этапе НЕ запущены.
    """
    settings = get_settings().kafka.consumer

    return dict(
        map(
            lambda topic: (
                topic[0],
                AIOKafkaConsumer(
                    topic[1],
                    bootstrap_servers=settings.bootstrap_servers,
                    group_id=settings.group_id,
                    key_deserializer=settings.key_deserializer,
                    value_deserializer=settings.value_deserializer
                )
            ),
            settings.topics.model_dump().items()
        )
    )
