FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bookscraper /app/bookscraper
COPY run_spider.sh /app/run_spider.sh

RUN chmod +x /app/run_spider.sh
