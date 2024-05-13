from typing import List, Union

from positronic_python.ai_interface import ai_enhanced, AiEnhanced


@ai_enhanced
class PromptEngineer:
    """
     You are an experienced prompt engineer
     You will be provided with a task, your job is to write a prompt that will guide another LLM model through the task
     Be resourceful, make sure the model has anything it needs to perform the task
    """

    thoughts: str
    missing_information: List[str]  # Questions that would help you to create a better prompt
    information_that_the_model_will_need: List[str]  # Pieces of the original input that are needed to perform the task

    """
    The `prompt` field will be forwarded as is to an LLM that will perform the task.
    Your prompt should be self-contained and include all the details needed to perform the task.
    The prompt must contain everything listed in `information_that_the_model_will_need` field
    Length: 10 - 1000 words
    """
    prompt: str  # instructions for the model


def generate_as_html(input: str):
    prompt: Union[PromptEngineer, AiEnhanced] = PromptEngineer.generate(input)
    thoughts = '\n'.join(prompt.information_that_the_model_will_need)
    questions = '\n'.join(prompt.missing_information)
    result = f"""
<b>Here are my thoughts:</b> 
{prompt.thoughts}

<b>Here are the questions I have about the task:</b>
{questions}
    
<b>The model will need the following information:</b> 
{thoughts}
    
<b>The prompt:</b> 
<code>{prompt.prompt}</code>
    """
    return result

if __name__ == "__main__":
    prompt = """Write a java class that implements this interface:

```package com.everc.marketview.regressionservice.services.impl;

public interface IDatabricksClient {

    String getNotebookTemplate(String notebookPath);
    
    void createNotebook(String notebookPath, String notebookSource);
    
    long getNotebookId(String notebookPath);
}```

    }```
    """

    generated_prompt : AiEnhanced = PromptEngineer.generate(prompt)

