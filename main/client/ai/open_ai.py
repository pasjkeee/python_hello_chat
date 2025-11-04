import logging as log
from typing import Annotated

import rich
from fastapi import Depends
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from main.model.open_ai.model import CreateClientInfoRs
from ..client import get_open_ai_client

create_client_info_system_prompt = """
            You are a helpful personality generator.
            Your task is to create an identity using the login field.
            You need to generate a person's gender and age, and based on that, their name, surname, and short personality description.
            """

create_client_info_user_prompt = lambda login: f"login is {login}"

class OpenAiCreateClientInfo:

    async def create_client_info(self, login: str) -> CreateClientInfoRs:
        log.info(f"Запрос на создание личности пользователя {login}")
        completion = get_open_ai_client().chat.completions.parse(
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

OpenAiCreateClientInfoDepends = Annotated[OpenAiCreateClientInfo, Depends()]