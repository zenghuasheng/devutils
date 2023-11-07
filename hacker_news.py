from langchain.document_loaders import HNLoader
loader = HNLoader("https://news.ycombinator.com/item?id=34817881")
data = loader.load()
print(data)