FROM python:3.12-alpine
LABEL org.opencontainers.image.source=https://github.com/skoval67/easy_bot

WORKDIR /app

COPY . .
RUN pip install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3", "main.py"]
