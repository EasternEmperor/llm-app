# 将LLM接入LangChain
1. 提示词模板：预先定义好提示词模板，将用户输入嵌入模板中完成功能：
```
# 这里我们要求模型对给定文本进行中文翻译
prompt = """请你将由三个反引号分割的文本翻译成英文！\
text: ```{text}```
"""
```
2. `LCEL(LangChain Expression Language, LangChain的表达式语言)`：`chain = prompt | model | output_parser`