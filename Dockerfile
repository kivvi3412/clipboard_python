# 使用官方Python镜像作为基础镜像
FROM python:3.10-bullseye

# 设置工作目录为/app
WORKDIR /app

# 将当前目录内容复制到容器中的/app
COPY . /app

# 升级pip并安装Python依赖项
RUN pip install --no-cache-dir --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 迁移数据库（根据需要执行）
RUN python manage.py makemigrations && \
    python manage.py migrate

# 对外暴露端口8000
EXPOSE 8000

# 定义环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 启动Django应用
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers=3", "--threads=3", "--worker-connections=1000", "clipboard.wsgi:application"]
