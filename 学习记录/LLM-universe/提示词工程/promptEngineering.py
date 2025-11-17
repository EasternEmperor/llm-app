"""
# This code is a simple example of how to use the Coze API to get a response from a chatbot.
"""

import os
import json

from cozepy import Coze, TokenAuth, Message, ChatEventType, COZE_CN_BASE_URL

class Prompt:
    def __init__(self):
        self.prompt = ""

    def set_prompt(self, prompt):
        self.prompt = prompt
    
    def get_prompt(self):
        return self.prompt
    
def get_coze_api_token(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('token='):
                return line.strip().split('=', 1)[1]
    raise ValueError("token not found in token.env")

def get_completion(prompt):
    coze_api_token = get_coze_api_token('/root/llmapp/学习记录/token.env')
    bot_id = '7535126454850748451'
    coze_api_base = COZE_CN_BASE_URL
    coze = Coze(
        auth=TokenAuth(coze_api_token),
        base_url=coze_api_base)

    response = ''
    for event in coze.chat.stream(bot_id=bot_id, user_id='user_1234567890', 
                                additional_messages=[Message.build_user_question_text(prompt)]
                                ):
        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
            response += event.message.content
        if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
            print('Chat completed.')
            print("token usage:", event.chat.usage.token_count)
    return response

if __name__ == "__main__":
    prompt = "What is the capital of France?"
    response = get_completion(prompt)
    print("Response:", response)

    # 从prompts.json文件中读取提示词
    prompts_file = 'prompts.json'
    if os.path.exists(prompts_file):
        with open(prompts_file, 'r', encoding='utf-8') as file:
            # json中是一个列表[]，其中每个元素结构是{"prompt": "提示词内容"}
            prompts_data = json.load(file)
        for item in prompts_data:
            if 'prompt' in item:
                prompt_text = item['prompt']
                print(f"Prompt: {prompt_text}")
                response = get_completion(prompt_text)
                print("Response:", response, end='\n\n')
            else:
                print("No 'prompt' key found in item:", item)
    else:
        print(f"File {prompts_file} does not exist.")