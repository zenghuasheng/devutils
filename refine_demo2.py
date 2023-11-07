from langchain import PromptTemplate, LLMChain
from langchain.chains.summarize import load_summarize_chain

# Load LLM and chain
llm = LLMChain()
chain = load_summarize_chain(llm, chain_type="refine")

# Input documents
docs = [
    "Doc 1 text...",
    "Doc 2 text...",
    "..."
]

# Prompt templates
prompt = PromptTemplate("Summarize the documents: {docs}")
refine_prompt = PromptTemplate("Refine summary: {summary} {docs}")

# Run chain
result = chain(
    docs=docs,
    question_prompt=prompt,
    refine_prompt=refine_prompt
)

print(result)