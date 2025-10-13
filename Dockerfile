# Dockerfile (单容器, 端口 8095)

# 使用包含 Python 的 Debian 基础镜像
FROM python:3.11-slim

# 1. 安装 Nginx 和 Supervisor
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    # 清理安装缓存
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/log/supervisor /var/log/nginx /var/log/gunicorn

# 2. 安装 Python 依赖
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 复制应用代码和配置
COPY . /app/
# 复制 Nginx 配置文件到 Nginx 配置目录
COPY default.conf /etc/nginx/sites-enabled/
# 复制 Supervisor 配置文件
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 移除 Nginx 默认配置
RUN rm /etc/nginx/sites-enabled/default

# 4. 暴露容器端口 (此端口应与 default.conf 中监听的端口一致)
EXPOSE 8095

# 5. 启动 Supervisor 作为容器主进程
# Supervisor 会自动启动 Nginx (8095) 和 Gunicorn (5000)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
