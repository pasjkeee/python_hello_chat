from typing import Callable, Any

from orjson import orjson as json
from pydantic import Field, BaseModel


def _default_json(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class Topics(BaseModel):
    """
    Настройки топиков
    """
    default: str = Field('default.topic.msg')


class ProducerKafkaSettings(BaseModel):
    """
    Настройки продьюсера
    """
    bootstrap_servers: str = Field('localhost:9092')
    client_id: str = Field('hello_chat')
    acks: str = Field('all')
    value_serializer: Callable[[Any], bytes] = Field(
        default_factory=lambda: (lambda v: json.dumps(v, default=_default_json)))
    key_serializer: Callable[[str], bytes] = Field(default_factory=lambda: (lambda k: k.encode()))
    topics: Topics = Field(default_factory=Topics)


class ConsumerKafkaSettings(BaseModel):
    """
    Настройки консьюмера
    """
    bootstrap_servers: str = Field('localhost:9092')
    group_id: str = Field('hello_chat')
    value_deserializer: Callable[[bytes], Any] = Field(default_factory=lambda: (lambda v: json.loads(v)))
    key_deserializer: Callable[[bytes], str] = Field(default_factory=lambda: (lambda k: k.decode()))
    topics: Topics = Field(default_factory=Topics)


class KafkaSettings(BaseModel):
    """
    Настройки kafka
    """
    producer: ProducerKafkaSettings = Field(default_factory=ProducerKafkaSettings)
    consumer: ConsumerKafkaSettings = Field(default_factory=ConsumerKafkaSettings)
