FROM docker.io/library/python:3.13-slim
# FROM docker.m.daocloud.io/library/python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

# 容器启动时自动建库（简化操作，生产应该用 init job 或迁移镜像）
RUN python manage.py migrate --noinput

EXPOSE 8000

#  1 worker + 4 threads，解决指标聚合问题
CMD ["gunicorn", "demo.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "1", "--threads", "4"]
