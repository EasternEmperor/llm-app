from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

def load_pdf(file_path):
    # 创建PyMuPDFLoader实例，加载PDF文件
    loader = PyMuPDFLoader(file_path)
    pdf_pages = loader.load()
    print(f"载入后的变量类型为：{type(pdf_pages)}，该PDF一共有{len(pdf_pages)}页。")
    # 打印每一页的内容
    for i, pdf_page in enumerate(pdf_pages):
        if i < 2:
            print(f"{i}: 每一个元素的类型：{type(pdf_page)}.\n该文档的描述性数据：{pdf_page.metadata}\n查看该文档的内容：{pdf_page.page_content}")
            print("-------------\n")
    return pdf_pages

def clean_data(pdf_pages):
    cleaned_pages = []
    for page in pdf_pages:
        content = page.page_content
        # 示例清洗操作：去除多余的空白行和修正换行符
        cleaned_content = "\n".join([line.strip() for line in content.splitlines() if line.strip()])
        pattern = re.compile(r'[^\u4e00-\u9fff](\n)[^\u4e00-\u9fff]', re.DOTALL)
        cleaned_content = re.sub(pattern, lambda match: match.group(0).replace('\n', ''), cleaned_content)
        cleaned_content = cleaned_content.replace(' +', '')
        cleaned_content = cleaned_content.replace('\n\n', '\n')
        page.page_content = cleaned_content
        cleaned_pages.append(page)
    page = cleaned_pages[1]
    print(f"清洗后的第二页内容为：\n{page.page_content}")

    return cleaned_pages

# 知识库中单段文本长度
CHUNK_SIZE = 500

# 知识库中相邻文本重合长度
OVERLAP_SIZE = 50

''' 
* RecursiveCharacterTextSplitter 递归字符文本分割
RecursiveCharacterTextSplitter 将按不同的字符递归地分割(按照这个优先级["\n\n", "\n", " ", ""])，
    这样就能尽量把所有和语义相关的内容尽可能长时间地保留在同一位置
RecursiveCharacterTextSplitter需要关注的是4个参数：

* separators - 分隔符字符串数组
* chunk_size - 每个文档的字符数量限制
* chunk_overlap - 两份文档重叠区域的长度
* length_function - 长度计算函数
'''
def split_documents(pdf_pages):
    # 使用递归字符文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = OVERLAP_SIZE
    )
    print(text_splitter.split_text(pdf_pages[1].page_content[0:1000]))
    split_docs = text_splitter.split_documents(pdf_pages)
    print(f"分割后的文档数量为：{len(split_docs)}")
    print(f"切分后的字符数（用来大致评估token数）：{sum([len(doc.page_content) for doc in split_docs])}")
    return split_docs


if __name__ == "__main__":
    # 1. 加载pdf文件
    file_path = "../knowledgebase/设计数据密集型应用@www.java1234.com.pdf"
    pdf_pages = load_pdf(file_path)
    # 2. 数据清洗
    cleaned_pages = clean_data(pdf_pages)
    # 3. 文档分割
    split_docs = split_documents(cleaned_pages)