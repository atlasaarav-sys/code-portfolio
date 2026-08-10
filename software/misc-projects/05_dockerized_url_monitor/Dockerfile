FROM python:3.12-slim

WORKDIR /app
COPY . .

EXPOSE 8080
ENV MONITOR_URLS=""

CMD ["python", "status_server.py", "--port", "8080", "--interval", "60"]
