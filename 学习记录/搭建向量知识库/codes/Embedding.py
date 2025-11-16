import requests
import json

def get_api_key(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('ApiKey='):
                return line.strip().split('=', 1)[1]
    raise ValueError("ApiKey not found in token.env")

def wenxin_embedding(text: str):
    # 读取token.env
    url = "https://qianfan.baidubce.com/v2/embeddings"
    api_key = get_api_key('/root/llmapp/学习记录/token.env')

    payload = json.dumps({
        "model": "embedding-v1",
        "input": [text]
    }, ensure_ascii=False)
    headers = {
        'appid': '',
        'Authorization': 'Bearer ' + api_key
    }

    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))

    return json.loads(response.text)

def embedding_func(texts: list):
    """
    批量获取文本的embedding
    :param texts: 文本列表
    :return: embedding列表
    """
    return [wenxin_embedding(text)['data'][0]['embedding'] for text in texts]

from langchain.embeddings.base import Embeddings

class WenxinEmbeddings(Embeddings):
    """
    使用文心向量API的自定义Embedding类
    """
    def embed_documents(self, texts):
        # 返回一个二维list，每个元素是一个文本的embedding
        return embedding_func(texts)

    def embed_query(self, text):
        # 单个文本的embedding
        return wenxin_embedding(text)['data'][0]['embedding']

if __name__ == "__main__":
    # 测试代码

    text = "你好，世界！"
    embedding_result = wenxin_embedding(text)


    print("本次embedding id:", embedding_result.get("id"))
    print("本次embedding产生时间戳:", embedding_result.get("created"))
    print('返回的embedding类型为:{}'.format(embedding_result['object']))
    print('embedding长度为：{}'.format(len(embedding_result['data'][0]['embedding'])))
    print('embedding（前10）为：{}'.format(embedding_result['data'][0]['embedding'][:10]))
