import requests
import json

def wenxin_embedding(text: str):
    api_key = "bce-v3/ALTAK-TMEZTMkQpAndVoYKxsWYz/d61aad9b630ef882e3d857b9bf35ff609468cb36"
    url = "https://qianfan.baidubce.com/v2/embeddings"

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


text = "你好，世界！"
embedding_result = wenxin_embedding(text)


print("本次embedding id:", embedding_result.get("id"))
print("本次embedding产生时间戳:", embedding_result.get("created"))
print('返回的embedding类型为:{}'.format(embedding_result['object']))
print('embedding长度为：{}'.format(len(embedding_result['data'][0]['embedding'])))
print('embedding（前10）为：{}'.format(embedding_result['data'][0]['embedding'][:10]))
