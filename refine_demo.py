from langchain.chains import QAWithSourcesChain
from langchain.llms.openai import OpenAI
from langchain.document_loaders.fs.text import TextLoader
from langchain.vectorstores.memory import MemoryVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate

questionPromptTemplateString = """Context information is below.
---------------------
{context}
---------------------
Given the context information and not prior knowledge, answer the question: {question}"""

questionPrompt = PromptTemplate(
    input_variables=["context", "question"],
    template=questionPromptTemplateString
)

refinePromptTemplateString = """The original question is as follows: {question}
We have provided an existing answer: {existing_answer}
We have the opportunity to refine the existing answer
(only if needed) with some more context below.
------------
{context}
------------
Given the new context, refine the original answer to better answer the question.
You must provide a response, either the original answer or a refined answer."""

refinePrompt = PromptTemplate(
    input_variables=["question", "existing_answer", "context"],
    template=refinePromptTemplateString
)

# Create the models and chain
embeddings = OpenAIEmbeddings()
model = OpenAI(temperature=0)
chain = QAWithSourcesChain(model, {
    "questionPrompt": questionPrompt,
    "refinePrompt": refinePrompt,
})

# Load the documents and create the vector store
loader = TextLoader("./state_of_the_union.txt")
docs = loader.loadAndSplit()
store = MemoryVectorStore.from_documents(docs, embeddings)

# Select the relevant documents
question = "What did the president say about Justice Breyer"
relevantDocs = store.similaritySearch(question)

# Call the chain
res = chain.call({
    "input_documents": relevantDocs,
    "question": question,
})

print(res)
