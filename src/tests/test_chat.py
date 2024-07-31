import os

import pytest
from openai.types.chat import ChatCompletion
from pydantic import BaseModel, Field

from ai import get_completions
from utils import settings

messages = [{"role": "system", "content": "You are a helpful assistant."}]
inputs = {
    "messages": messages,
    "azure_openai_deployment_name": settings.AZURE_OPENAI_DEPLOYMENT_NAME,
    "azure_openai_endpoint": settings.AZURE_OPENAI_ENDPOINT,
    "azure_openai_api_key": settings.AZURE_OPENAI_API_KEY,
    "azure_openai_api_version": settings.AZURE_OPENAI_API_VERSION,
}

print(f" working directory: {os.getcwd()}")


def test_get_chat_completions():
    response = get_completions(
        **inputs,
        stream=False,
    )

    assert len(response) > 0
    assert type(response) == str


def test_get_chat_completions_model():
    global messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Le numéro de compte est 208977"},
    ]

    class UserInfo(BaseModel):
        number_account: str = Field(default=None, description="Le numéro de compte du client")

    response = get_completions(**inputs, stream=False, response_model=UserInfo)

    assert isinstance(response, UserInfo)


def test_get_chat_completions_full_response():
    response = get_completions(**inputs, stream=False, full_response=True)
    print(f"full response: {response}")
    print(f"full response: {type(response)}")
    assert response is not None
    assert type(response) == ChatCompletion


def test_get_chat_completions_exception():
    with pytest.raises(NotImplementedError):
        get_completions(
            **inputs,
            stream=True,
        )


def test_get_chat_completions_none():
    global inputs
    inputs["messages"] = None

    with pytest.raises(NotImplementedError):
        response = get_completions(
            **inputs,
            stream=True,
        )
        assert response is None
