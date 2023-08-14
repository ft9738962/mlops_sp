# 使用 Ubuntu 22.04 作为基础镜像
FROM ubuntu:22.04

# 更新软件源并安装必要的软件
RUN apt-get update

# 安装 Python 3.10 & GIT
RUN apt-get install -y python3.10
RUN apt-get install -y python3-pip
RUN apt-get install -y git

# 设置 Python 3.10 为默认的 Python 版本
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# 创建 work 文件夹
RUN mkdir /work

# 将本地文件夹复制到容器的 /work 目录下
COPY src /work/src
COPY scripts /work/scripts
COPY requirements.txt /work

# 运行训练脚本并打开MLFLOW UI
RUN chmod +x /work/scripts/*

ENTRYPOINT /work/scripts/train.sh
