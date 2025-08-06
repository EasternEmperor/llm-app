# 大模型应用开发(LLM-app)
1. 参考内容：https://github.com/datawhalechina/llm-universe
2. linux安装`conda`:
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```
3. 环境配置：
```
# 1. 克隆项目
conda create -n llm python=3.10
conda activate llm
git clone git@github.com:datawhalechina/llm-universe.git

# 2. 安装包
cd llm-universe
pip install -r requirements.txt
# 清华源加速
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```