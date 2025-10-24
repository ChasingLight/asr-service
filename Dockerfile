# base image
FROM python:3.12.11-slim-bookworm AS base

# 设置工作目录
WORKDIR /asr_service

# 安装 uv 包管理工具
ENV UV_VERSION=0.7.11
RUN pip install --no-cache-dir uv==${UV_VERSION} -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


# ------------------Step1：依赖构建阶段------------------
FROM base AS packages

# 安装 python 依赖
COPY pyproject.toml uv.lock ./
ENV UV_HTTP_TIMEOUT=600
RUN uv sync --frozen --no-dev -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


# ------------------Step2：运行镜像阶段------------------
FROM base AS production

# 安装 vim 等常见命令工具
RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl telnet vim

# 设置时区
ENV TZ=Asia/Shanghai

# 拷贝项目代码
WORKDIR /asr_service/app
COPY . /asr_service

# 拷贝 uv 虚拟环境
ENV VIRTUAL_ENV=/asr_service/.venv
COPY --from=packages ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# 容器启动后默认执行命令由 docker-compose 决定
#ENTRYPOINT ["bash", "-c"]