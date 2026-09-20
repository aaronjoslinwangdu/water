FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.12.17 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY leader/pyproject.toml ./leader/
COPY node/pyproject.toml ./node/
RUN uv sync --package leader --no-dev --frozen --no-cache 
COPY leader/src ./leader/src/

EXPOSE 80

CMD ["/app/.venv/bin/fastapi", "run", "leader/src/main.py", "--port", "80", "--host", "0.0.0.0"]
