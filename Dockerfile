FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PYTHONPATH=/app/src

WORKDIR /app

COPY pyproject.toml README.md ./
RUN mkdir -p src && pip install --no-cache-dir .

CMD ["python", "src/init.py"]
