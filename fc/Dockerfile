FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:${PATH}"

# 固定版本 uv
COPY --from=ghcr.io/astral-sh/uv:0.7.3 /uv /usr/local/bin/uv

# 先装依赖（利用 Docker 缓存层）
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# 复制项目源码
COPY miyouqian/ ./miyouqian/
COPY main.py .
COPY config.example.yaml .

# 阿里云 FC 专用入口
COPY fc/entrypoint.sh /entrypoint.sh
COPY fc/server.py /server.py
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

# FC 自定义容器要求监听 9000 端口（CAPort 默认值）
EXPOSE 9000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "/server.py"]
