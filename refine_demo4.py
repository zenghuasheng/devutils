from langchain.chains import ReduceDocumentsChain, MapReduceDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter

loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
docs = loader.load()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
# chain = load_summarize_chain(llm, chain_type="stuff")

# chain.run(docs)
# print(len(docs))


from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
#
# # Define prompt
# prompt_template = """Write a concise summary of the following:
# "{text}"
# CONCISE SUMMARY:"""
# prompt = PromptTemplate.from_template(prompt_template)
#
# # Define LLM chain
# llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
# llm_chain = LLMChain(llm=llm, prompt=prompt)
#
# # Define StuffDocumentsChain
# stuff_chain = StuffDocumentsChain(
#     llm_chain=llm_chain, document_variable_name="text"
# )
#
# docs = loader.load()
# print(stuff_chain.run(docs))

from langchain.chains.mapreduce import MapReduceChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ReduceDocumentsChain, MapReduceDocumentsChain

# llm = ChatOpenAI(temperature=0)

# Map
map_template = """The following is a set of documents
{docs}
Based on this list of docs, please identify the main themes 
Helpful Answer:"""
map_prompt = PromptTemplate.from_template(map_template)
map_chain = LLMChain(llm=llm, prompt=map_prompt)

# Reduce
reduce_template = """The following is set of summaries:
{doc_summaries}
Take these and distill it into a final, consolidated summary of the main themes. 
Helpful Answer:"""
reduce_prompt = PromptTemplate.from_template(reduce_template)
reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

# Takes a list of documents, combines them into a single string, and passes this to an LLMChain
combine_documents_chain = StuffDocumentsChain(
    llm_chain=reduce_chain, document_variable_name="doc_summaries"
)

# Combines and iteravely reduces the mapped documents
reduce_documents_chain = ReduceDocumentsChain(
    # This is final chain that is called.
    combine_documents_chain=combine_documents_chain,
    # If documents exceed context for `StuffDocumentsChain`
    collapse_documents_chain=combine_documents_chain,
    # The maximum number of tokens to group documents into.
    token_max=4000,
)

# Combining documents by mapping a chain over them, then combining results
map_reduce_chain = MapReduceDocumentsChain(
    # Map chain
    llm_chain=map_chain,
    # Reduce chain
    reduce_documents_chain=reduce_documents_chain,
    # The variable name in the llm_chain to put the documents in
    document_variable_name="docs",
    # Return the results of the map steps in the output
    return_intermediate_steps=False,
)

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000, chunk_overlap=0
)
split_docs = text_splitter.split_documents(docs)

print(map_reduce_chain.run(split_docs))


#
# Created a chunk of size 1003, which is longer than the specified 1000
#
#
# The main themes identified in the provided set of documents are:
#
# 1. LLM-powered autonomous agent systems: The documents discuss the concept of building autonomous agents with large language models (LLMs) as the core controller. They explore the potential of LLMs beyond content generation and present them as powerful problem solvers.
#
# 2. Components and capabilities of the agent systems: The documents outline the key components of LLM-powered agent systems, including planning, memory, and tool use. Each component is described in detail, highlighting its role in enhancing the agent's capabilities.
#
# 3. Planning and task decomposition: The planning component focuses on task decomposition and self-reflection. The agent breaks down complex tasks into smaller subgoals and learns from past actions to improve future results.
#
# 4. Memory and learning: The memory component includes short-term memory for in-context learning and long-term memory for retaining and recalling information over extended periods. The use of external vector stores for fast retrieval is also mentioned.
#
# 5. Tool use and external APIs: The agent learns to utilize external APIs for accessing additional information, executing code, and leveraging proprietary information sources that may not be available in the model weights.
#
# 6. Case studies and proof-of-concept examples: The documents provide examples of how LLM-powered agents can be applied in various domains, such as scientific discovery, generative agents simulation, and chemistry. These case studies demonstrate the practical applications of the agent systems.
#
# 7. Challenges and limitations: The documents acknowledge the challenges associated with building and utilizing LLM-powered autonomous agents, such as the limitations of finite context length, long-term planning, and the reliability of natural language interfaces.
#
# 8. Steerability and prompting: The concept of steerability in language models and the use of prompts to elicit specific responses and improve performance are discussed in some documents.
#
# 9. NLP and vector search: The field of natural language processing (NLP) and efficient vector similarity search techniques are mentioned in relation to LLM-powered agent systems.
#
# 10. GitHub repositories and resources: Several GitHub repositories and resources related to LLMs, NLP, and agent systems are mentioned in the documents.
#
# These main themes provide an overview of the key concepts and topics discussed in the provided set of documents.
