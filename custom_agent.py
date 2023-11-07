import os

os.environ["SERPER_API_KEY"] = "735065c71e90ac915b3049a52ef766433d4c6962"

from langchain.agents import Tool, AgentExecutor, BaseSingleActionAgent
from langchain import OpenAI, SerpAPIWrapper
from langchain.utilities import GoogleSerperAPIWrapper

search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]

from langchain.chains.llm import LLMChain
from langchain.base_language import BaseLanguageModel
from typing import List, Tuple, Any, Union
from typing import Any, Callable, List, NamedTuple, Optional, Sequence
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts.prompt import PromptTemplate
from langchain.tools.base import BaseTool


PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""
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

def create_prompt(
        tools: Sequence[BaseTool],
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
) -> PromptTemplate:
    """Create prompt in the style of the zero shot agent.

    Args:
        tools: List of tools the agent will have access to, used to format the
            prompt.
        prefix: String to put before the list of tools.
        suffix: String to put after the list of tools.
        input_variables: List of input variables the final prompt will expect.

    Returns:
        A PromptTemplate with the template assembled from the pieces here.
    """
    tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
    tool_names = ", ".join([tool.name for tool in tools])
    format_instructions = format_instructions.format(tool_names=tool_names)
    template = "\n\n".join([prefix, tool_strings, format_instructions, suffix])
    if input_variables is None:
        input_variables = ["input", "agent_scratchpad"]
    return PromptTemplate(template=template, input_variables=input_variables)



class FakeAgent(BaseSingleActionAgent):
    """Fake Custom Agent."""

    @property
    def input_keys(self):
        return ["input"]

    def plan(
            self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        return AgentAction(tool="Search", tool_input=kwargs["input"], log="")

    async def aplan(
            self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        return AgentAction(tool="Search", tool_input=kwargs["input"], log="")

llm_chain = LLMChain(
    llm=BaseLanguageModel,
    prompt=create_prompt(tools),
)

agent = FakeAgent(
    llm_chain=llm_chain,
)
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
agent_executor.run("王楚钦目前世界排名")
