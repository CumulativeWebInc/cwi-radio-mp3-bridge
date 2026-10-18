FROM python:3.12-slim
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY server.py ./
ENV PORT=10000
EXPOSE 10000
CMD ["python3", "server.py"]
