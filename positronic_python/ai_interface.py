import dataclasses
import inspect
import json

import os
import webbrowser
import positronic_python.ai_service as ai_service

from schema import Message


class AiEnhanced:
    pass


prompt = "You are an advanced AI model tasked with generating a JSON output that can be deserialized to an instance of the following class. Your goal and character should be inferred from the source code and the comments present within the class.\n"


def ai_enhanced(cls) -> AiEnhanced:
    cls._system_prompt = prompt + inspect.getsource(cls)
    cls._source = inspect.getsource(cls)
    cls = dataclasses.dataclass(cls)

    # Define a new __init__ that prints the source and then calls the original __init__
    def generate(user_prompt: str):
        messages = [
            Message.system(cls._system_prompt),
            Message.user(user_prompt),
            ]
        res = ai_service.call_model(messages)
        res_json = json.loads(res)
        instance = cls(**res_json)
        instance._conversation = messages
        instance._original_user_prompt = user_prompt
        return instance

    def modify(self, instruction: str):
        modify_prompt = "Modify the object according to the following instruction:\n"
        messages = [
            Message.system(cls._system_prompt),
            Message.user(self._original_user_prompt),
            Message.assistant(json.dumps(dataclasses.asdict(self))),
            Message.user(modify_prompt + instruction),
        ]
        res = ai_service.call_model(messages)
        try:
            res_json = json.loads(res)
            instance = cls(**res_json)
        except Exception as e:
            print(str(e))
            messages.append(Message.user("Failed to deserialize the response. Please stay in character."))
            res = ai_service.call_model(messages)
            res_json = json.loads(res)
            instance = cls(**res_json)

        instance._conversation = messages
        instance._original_user_prompt = self._original_user_prompt
        return instance

    def to_html(self, render_in_browser=True, prompt:str = None) -> str:
        prompt_1 = "You are an advanced and resourceful AI model. Your task is to convert the following JSON object, which corresponds to the provided Python dataclass, into visually pleasing HTML5 page. Use Bootstrap (https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css, https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js)"
        prompt_2 = "Please generate a HTML5 page that presents this information in a user-friendly, visually pleasing and attractive manner."
        json_object = json.dumps(dataclasses.asdict(self))
        messages = [
            Message.system(f"{prompt_1}\nPython dataclass:\n{self._source}\nJSON object:\n{json_object}\n{prompt_2}")
        ]
        if prompt:
            messages.append(Message.user(prompt))

        html_content = ai_service.call_model(messages)
        if render_in_browser:
            with open('/tmp/temp.html', 'w') as f:
                f.write(html_content)
            # Get the full path of the file
            full_filename = os.path.abspath('/tmp/temp.html')

            # Open the file in the browser
            webbrowser.open('file://' + full_filename)
        return html_content

    cls.modify = modify
    cls.generate = generate
    cls.to_html = to_html

    return cls

@ai_enhanced
class TestClass:
    upper_case: str
    translation_to_hebrew: str
    short_story: str # Must be funny must contain the prompt and must contain the word "banana".


if __name__ == "__main__":

    x: TestClass = TestClass.generate("Hello world")

    html_content1 = x.to_html()

