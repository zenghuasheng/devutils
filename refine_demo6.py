from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate

# loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
loader = WebBaseLoader("https://juejin.cn/post/6844904185264095246")
docs = loader.load()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

questionPromptTemplateString = """Context information is below.
---------------------
{context}
---------------------
Given the context information and not prior knowledge, answer the question: {question}"""

prompt = PromptTemplate.from_template(questionPromptTemplateString)

refinePromptTemplateString = """The original question is as follows: {question}
We have provided an existing answer: {existing_answer}
We have the opportunity to refine the existing answer
(only if needed) with some more context below.
------------
{context}
------------
Given the new context, refine the original answer to better answer the question.
You must provide a response, either the original answer or a refined answer."""
refine_prompt = PromptTemplate.from_template(refinePromptTemplateString)

chain = load_summarize_chain(
    llm=llm,
    chain_type="refine",
    question_prompt=prompt,
    refine_prompt=refine_prompt,
    return_intermediate_steps=True,
    input_key="input_documents",
    output_key="output_text",
    document_variable_name="context",
    verbose=True,
)
# self_ask_with_search.agent.llm_chain.verbose = True
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000, chunk_overlap=0
)
question = "如何用CDN优化加载速度？"
split_docs = text_splitter.split_documents(docs)
result = chain({
    "input_documents": split_docs,
    "question": question,
}, return_only_outputs=True)
print(result["output_text"])
print("\n\n".join(result["intermediate_steps"][:3]))
