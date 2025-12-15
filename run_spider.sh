#!/bin/bash

echo "Waiting for Postgres..."
sleep 5

if [ -z "$URL" ]; then
  echo "ERROR: URL not provided. Pass it as environment variable URL=..."
  exit 1
fi

scrapy crawl books -a url="$URL"
