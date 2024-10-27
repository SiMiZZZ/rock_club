FROM python:3.12

RUN apt-get update \
	&& apt-get install -y --no-install-recommends

RUN pip install uv

WORKDIR /app

COPY src .
COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --frozen

