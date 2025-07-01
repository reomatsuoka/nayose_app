FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential fonts-ipafont-gothic && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "/app/src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]