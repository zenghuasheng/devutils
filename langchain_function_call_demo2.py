from typing import Optional

from langchain.chains.openai_functions import create_openai_fn_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from pydantic import BaseModel, Field


class OptionalFavFood(BaseModel):
    """Either a food or null."""

    food: Optional[str] = Field(
        None,
        description="Either the name of a food or null. Should be null if the food isn't known.",
    )


def record_person(name: str, age: int, fav_food: OptionalFavFood) -> str:
    """Record some basic identifying information about a person.

    Args:
        name: The person's name.
        age: The person's age in years.
        fav_food: An OptionalFavFood object that either contains the person's favorite food or a null value. Food should be null if it's not known.
    """
    return f"Recording person {name} of age {age} with favorite food {fav_food.food}!"


def record_dog(name: str, color: str, fav_food: OptionalFavFood) -> str:
    """Record some basic identifying information about a dog.

    Args:
        name: The dog's name.
        color: The dog's color.
        fav_food: An OptionalFavFood object that either contains the dog's favorite food or a null value. Food should be null if it's not known.
    """
    return f"Recording dog {name} of color {color} with favorite food {fav_food}!"


prompt_msgs = [
    SystemMessage(content="You are a world class algorithm for recording entities"),
    HumanMessage(
        content="Make calls to the relevant function to record the entities in the following input:"
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
    HumanMessage(content="Tips: Make sure to answer in the correct format"),
]
prompt = ChatPromptTemplate(messages=prompt_msgs)

llm = ChatOpenAI(model="gpt-3.5-turbo-16k-0613", temperature=0.5)
chain = create_openai_fn_chain([record_dog], llm, prompt, verbose=True)
res = chain.run(
    # "I can't find my dog Henry anywhere, he's a small brown beagle. Could you send a message about him?"
    # "The most important thing to remember about Tommy, my 12 year old, is that he'll do anything for apple pie."
    "介绍一下langchain"
)
print(res)
