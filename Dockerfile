FROM python:3.11-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt flask flask-cors

# 复制应用代码
COPY *.py index.html ./

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["python3", "app.py"]
