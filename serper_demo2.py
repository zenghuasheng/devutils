import os

os.environ["SERPER_API_KEY"] = "735065c71e90ac915b3049a52ef766433d4c6962"

from langchain.utilities import GoogleSerperAPIWrapper
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

llm = OpenAI(temperature=0)
search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="搜索引擎",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]

self_ask_with_search = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
self_ask_with_search.agent.llm_chain.verbose = True
# print(self_ask_with_search.agent.llm_chain.prompt.template)
self_ask_with_search.run(
    # "王楚钦目前的世界排名"
    "讲一个笑话"
)
