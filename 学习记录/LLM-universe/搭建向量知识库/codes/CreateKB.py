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
print(f"切分后的字符数（用来大致评估token数）：{sum([len(doc.page_content) for doc in split_docs])}")

# 构建Chroma向量数据库
# from langchain.embeddings.baidu_qianfan_endpoint import QianfanEmbeddingsEndpoint
# embedding = QianfanEmbeddingsEndpoint()
from Embedding import WenxinEmbeddings
from langchain_community.vectorstores import Chroma
# 初始化自定义embedding对象
wenxin_embed = WenxinEmbeddings()

persist_directory = '../vector_db/chroma'
# 从文档创建向量数据库，由向量数据库调用embedding方法
print("开始创建向量数据库...")
# vectordb = Chroma.from_documents(
#     documents=split_docs, 
#     embedding=wenxin_embed, 
#     persist_directory=persist_directory
# )
print("向量数据库创建完成！")

# 读取向量数据库
vectordb = Chroma(
    embedding_function=wenxin_embed, 
    persist_directory=persist_directory
)
print("向量库中存储的数量：", vectordb._collection.count())

# 向量检索
question = "什么是数据系统的可靠性"
print(f"\n\n检索问题：{question}")
sim_docs = vectordb.similarity_search(question, k=3)
print(f"检索到的文档数量：{len(sim_docs)}")
for i, sim_doc in enumerate(sim_docs):
    print(f"检索到的第{i+1}个文档：")
    print(f"文档内容：{sim_doc.page_content}")
    print(f"文档元数据：{sim_doc.metadata}")
    print("-" * 50)