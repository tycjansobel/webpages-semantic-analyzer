FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \ 
    libgl1-mesa-glx \
    build-essential \
    python3-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

RUN BLIS_ARCH="generic" pip install spacy --no-binary blis


RUN python -m spacy download pl_core_news_lg
RUN python -m spacy download pl_core_news_sm

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 3000

CMD ["fastapi", "run", "main.py", "--port=3000"]