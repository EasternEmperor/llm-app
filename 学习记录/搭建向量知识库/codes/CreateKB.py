import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader

# 加载文件
file_paths = []
folder_path = '/root/llmapp/学习记录/搭建向量知识库/knowledgebase'
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_paths.append(file_path)
print(file_paths[:])

# 加载知识库文件，存放在loaders里
loaders = []

for file_path in file_paths:
    file_type = file_path.split('.')[-1]
    if file_type == 'pdf':
        loaders.append(PyMuPDFLoader(file_path))
    elif file_type == 'md':
        loaders.append(UnstructuredMarkdownLoader(file_path))

# 加载文档
texts = []
for loader in loaders: texts.extend(loader.load())
# 查看文档
text = texts[0]
print(f"每一个元素的类型：{type(text)}.", 
    f"该文档的描述性数据：{text.metadata}", 
    f"查看该文档的内容:\n{text.page_content[0:]}", 
    sep="\n------\n")

# 切分文档
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200, 
    length_function=len
)
split_docs = text_splitter.split_documents(texts)

# 构建Chroma向量数据库
embedding = QianfanEmbeddingsEndpoint()
persist_directory = '../vector_db/chroma'

from langchain_community.vectorstores import Chroma
vectordb = Chroma.from_documents(
    documents=split_docs, 
    embedding=embedding, 
    persist_directory=persist_directory
)
print("向量库中存储的数量：", vectordb._collection.count())

