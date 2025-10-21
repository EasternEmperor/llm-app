from langchain_openai import ChatOpenAI
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint



llm = QianfanLLMEndpoint(streaming = True, api_key="bce-v3/ALTAK-7ALd9B14OLmUyqMrx2eKi/27d9a21194ebab4f3d52ba460d19d46271291c6c")
res = llm("你好，请你做个自我介绍！")
print(res)