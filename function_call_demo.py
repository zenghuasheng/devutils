import os

import openai
import json

from langchain.utilities import GoogleSerperAPIWrapper

os.environ["SERPER_API_KEY"] = "735065c71e90ac915b3049a52ef766433d4c6962"

s = GoogleSerperAPIWrapper()


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


def search(query: str) -> str:
    return s.run(query)


def run_conversation(question: str):
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": question}]
    functions = [
        # {
        #     "name": "get_current_weather",
        #     "description": "Get the current weather in a given location",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "location": {
        #                 "type": "string",
        #                 "description": "The city and state, e.g. San Francisco, CA",
        #             },
        #             "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        #         },
        #         "required": ["location"],
        #     },
        # },
        {
            "name": "search",
            "description": "useful for when the question you don't know, or about current events",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query string",
                    },
                },
                "required": ["query"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
        temperature=0.2
    )
    response_message = response["choices"][0]["message"]
    print(response_message.content)

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            # "get_current_weather": get_current_weather,
            "search": search,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            query=function_args.get("query"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response

        second_response_message = second_response["choices"][0]["message"]
        print("调用了函数")
        print(second_response_message.content)
        return second_response


run_conversation(
    # "What's the weather like in Boston?"
    "介绍一下clickhouse"
    # "马龙目前世界排名"
    # "你知道langchain吗? 不知道去搜索一下"
    # "介绍一下langchain"
)
