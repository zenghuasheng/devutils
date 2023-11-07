import os
import tomllib

import openai
import json

from typing import Optional
from pydantic import BaseModel
from pydantic import Field

os.environ["OPENAI_API_KEY"] = "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"


class Conversation(BaseModel):
    role: str = Field(..., description="角色")
    text: str = Field(..., description="文本")


class PromptObject(BaseModel):
    prompt_class: str = Field(..., description="Prompt class")
    read_history: bool = Field(..., description="Prompt read history")
    temperature: float = Field(..., description="Prompt temperature")
    system_msg: Optional[str] = Field(None, description="Prompt system message")
    max_tokens: Optional[int] = Field(None, description="Prompt max tokens")
    func_schema: Optional[str] = Field(None, description="Prompt function schema")
    func_name: Optional[str] = Field(None, description="Prompt function name")
    func_description: Optional[str] = Field(None, description="Prompt function description")
    text: Optional[str] = Field(None, description="Prompt text")
    variables: Optional[list[dict]] = Field(None, description="Prompt variables")
    conversations: Optional[list[Conversation]] = Field(None, description="Prompt conversations")
    reference_type: Optional[str] = Field(None, description="Prompt reference maker, see ReferenceMakerMap")
    accept_condition: Optional[str] = Field(None, description="Prompt accept condition")
    refine_prompt: Optional[str] = Field(None, description="Prompt refine prompt")


def get_latest_prompt():
    file_name = "./prompt.toml"
    with open(file_name, "rb") as f:
        return tomllib.load(f)


def load_latest_prompt_object() -> PromptObject:
    prompt_obj = get_latest_prompt()

    config = prompt_obj["config"]

    prompt_class = config["class"]
    prompt_temperature = config.get("temperature", 0.0)
    prompt_system_msg = config.get("system", None)
    max_tokens = config.get("max_length", None)
    reference_type = config.get("reference_type", None)
    read_history = config.get("read_history", False)
    accept_condition = config.get("accept_condition", None)
    refine_prompt = config.get("refine_prompt", None)

    function = prompt_obj.get("function", {})
    func_schema = function.get("schema", None)
    func_name = function.get("name", None)
    func_description = function.get("description", None)

    prompt = prompt_obj.get("prompt", {})
    prompt_variables = prompt.get("variables", [])

    prompt_text = prompt["text"] if "text" in prompt else None
    prompt_conversations = (
        [
            Conversation(
                role=c["role"],
                text=c["text"],
            )
            for c in prompt_obj["conversations"]
        ]
        if "conversations" in prompt_obj
        else []
    )

    return PromptObject(
        prompt_class=prompt_class,
        temperature=prompt_temperature,
        read_history=read_history,
        reference_type=reference_type,
        system_msg=prompt_system_msg,
        max_tokens=max_tokens,
        func_schema=func_schema,
        func_name=func_name,
        func_description=func_description,
        variables=prompt_variables,
        text=prompt_text,
        conversations=prompt_conversations,
        accept_condition=accept_condition,
        refine_prompt=refine_prompt,
    )


def run_conversation(variables: dict):
    # Step 1: send the conversation and available functions to GPT
    prompt_object = load_latest_prompt_object()

    formatted_template = prompt_object.text.format(**variables)
    messages = [
        {"role": "system", "content": prompt_object.system_msg},
        {"role": "user", "content": formatted_template},
    ]

    schema_dict = json.loads(prompt_object.func_schema)
    functions = [
        {
            "name": prompt_object.func_name,
            "description": prompt_object.func_description,
            "parameters": schema_dict,
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call={"name": prompt_object.func_name},  # auto is default, but we'll be explicit
        temperature=prompt_object.temperature
    )
    response_message = response["choices"][0]["message"]
    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        function_args = json.loads(response_message["function_call"]["arguments"])
        formatted_json = json.dumps(function_args, indent=4, ensure_ascii=False)
        # 打印格式化后的 JSON 字符串
        print(formatted_json)
    else:
        print("没有调用函数")


run_conversation(
    {
        "input": "",
        "language": "zh",
    }
)
