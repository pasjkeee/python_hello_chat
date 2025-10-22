import rich
import logging as log
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from src.client import open_ai_client
from src.model.open_ai.model import CreateClientInfoRs

create_client_info_system_prompt = """
            You are a helpful personality generator.
            Your task is to create an identity using the login field.
            You need to generate a person's gender and age, and based on that, their name, surname, and short personality description.
            """

create_client_info_user_prompt = lambda login: f"login is {login}"


async def create_client_info(login: str) -> CreateClientInfoRs:
    log.info(f"Запрос на создание личности пользователя {login}")
    completion = open_ai_client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            ChatCompletionSystemMessageParam(role="system", content=create_client_info_system_prompt),
            ChatCompletionUserMessageParam(role="user", content=create_client_info_user_prompt(login)),
        ],
        response_format=CreateClientInfoRs,
    )

    response = completion.choices[0].message
    if response.parsed:
        rich.print(response.parsed)
        log.info(f"Запрос на создание личности пользователя выполнен: {response.parsed}")
        return response.parsed
    else:
        raise RuntimeError
