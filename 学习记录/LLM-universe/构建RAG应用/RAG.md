# 将LLM接入LangChain
## 检索链
1. 提示词模板：预先定义好提示词模板，将用户输入嵌入模板中完成功能：
```
# 这里我们要求模型对给定文本进行中文翻译
prompt = """请你将由三个反引号分割的文本翻译成英文！\
text: ```{text}```
"""
```
2. `LCEL(LangChain Expression Language, LangChain的表达式语言)`：`chain = prompt | model | output_parser`
3. LLM对于一些时效性强的问题或者非常识性的专业问题，回答得并不是很好；而加上知识库就可以帮助LLM做出更好的回答，也有助于缓解大模型的“幻觉”问题

## 向检索链添加聊天记录
1. 带历史记录的问答链
```
from langchain_core.prompts import ChatPromptTemplate

# 问答链的系统prompt
system_prompt = (
    "你是一个问答任务的助手。 "
    "请使用检索到的上下文片段回答这个问题。 "
    "如果你不知道答案就说不知道。 "
    "请使用简洁的话语回答用户。"
    "\n\n"
    "{context}"
)
# 制定prompt template
qa_prompt = ChatPromptTemplate(
    [
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)
```
2. 通过历史记录上下文，让LLM自动完善用户的问题（比如一些代词、名词的含义等）
    - 看来现在的各种聊天LLM使用的就是这样的方式实现上下文记忆的