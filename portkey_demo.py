from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
import openai

openai.api_base = "https://api.portkey.ai/v1/proxy"

llm = OpenAI(temperature=0,
             openai_api_key="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",
             headers={
                 "x-portkey-api-key": "55+6a17IO0Z2GyvdrmpFBiVlMrc=",
                 "x-portkey-mode": "proxy openai",
                 "x-portkey-trace-id": "e4bbb7c0f6a2ff08"
             }, user="testing_traces")

tools = load_tools(["llm-math"], llm=llm)

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.run("What is 56 multiplied by 17654 to the 0.43 power?")
