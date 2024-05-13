import logging
from typing import List

import openai.types
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from tenacity import wait_random_exponential, retry, stop_after_attempt

import configs_reader
from positronic_python.schema import Message, UserRole

client = OpenAI(
    # This is the default and can be omitted
    api_key=configs_reader.open_ai_token,
)
model = "gpt-4-turbo"
# model = "gpt-3.5-turbo"
# model = "gpt-3.5-turbo-16k"


@retry(wait=wait_random_exponential(multiplier=1, max=10), stop=stop_after_attempt(3))
def call_model(messages: List[Message], force_json = True) -> str:
    logging.info(f"using {model} model")
    messages_dict = [m.to_dict() for m in messages]
    response_format = { "type": "json_object" } if force_json else None
    response = client.chat.completions.create(
        model=model,
        messages=messages_dict,
        temperature=0,
        stream=True,
        response_format=response_format,
    )
    response_text: str = ""

    for chunk in response:
        chunk_message = chunk.choices[0].delta  # extract the message
        chunk_text = chunk_message.content
        if chunk_text and len(chunk_text) > 0:
            print(chunk_text, end='', flush=True)
            response_text += chunk_text
    #logging.info(f"used {response.usage['total_tokens']} tokens")
    #response: str = response.choices[0]['message']["content"]
    messages.append(Message(role=UserRole.ASSISTANT, content=response_text))
    return response_text


def call_model_with_prompt(prompt: str, force_json=False) -> str:
    messages = [Message(role=UserRole.USER, content=prompt)]
    return call_model(messages, force_json=force_json)
