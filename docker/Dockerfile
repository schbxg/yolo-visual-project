# YOLO Training Docker Image
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    wget \
    curl \
    vim \
    htop \
    tree \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 升级pip并安装Python依赖
RUN pip3 install --upgrade pip

# 安装PyTorch (CUDA版本)
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装YOLO和计算机视觉库
RUN pip3 install ultralytics \
    opencv-python \
    pillow \
    matplotlib \
    seaborn \
    tqdm \
    numpy \
    pandas \
    scikit-learn \
    tensorboard

# 创建工作目录
WORKDIR /workspace

# 复制项目文件
COPY . .

# 设置默认命令
CMD ["python3", "scripts/train.py"]
