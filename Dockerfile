FROM python:3.12-alpine AS base
LABEL org.opencontainers.image.source=https://github.com/skoval67/easy_bot

WORKDIR /app

COPY . .
RUN pip install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3", "main.py"]

FROM base AS debug
RUN pip install debugpy
ENTRYPOINT [ "python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "main.py" ]