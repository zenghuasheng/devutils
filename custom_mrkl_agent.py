import os

from langchain import OpenAI, LLMChain
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.utilities import GoogleSerperAPIWrapper

os.environ["SERPER_API_KEY"] = "735065c71e90ac915b3049a52ef766433d4c6962"

search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    )
]

# prefix = """Answer the following questions as best you can, but speaking as a pirate might speak. You have access to the following tools:"""
# suffix = """Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Args"
#
# Question: {input}
# {agent_scratchpad}"""


PREFIX = """Answer general questions with your knowledge base, but utilize the search tool for specific or real-time data. You have access to the following tools:"""
FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""
SUFFIX = """Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools, prefix=PREFIX, suffix=SUFFIX, format_instructions = FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad"]
)

print(prompt.template)

llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)

tool_names = [tool.name for tool in tools]
agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
agent.llm_chain.verbose = True

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)

agent_executor.run(
    "1+1=? 不要搜索，自己算"
)

