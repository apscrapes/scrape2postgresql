# 🕷️ scrape2postgresql

`scrape2postgresql` is a **demo project** that shows how to use **Scrapy** to scrape web pages and store **structured data** in a **PostgreSQL** database using **Docker**.

The goal of this project is :
- to understand how Scrapy works in real projects
- to learn how to persist scraped data properly
- to follow industry-style containerized workflows
- to avoid common beginner mistakes in scraping setups

This project uses **books.toscrape.com** as a safe, public demo website.

---

## 🚀 What this project does

- Scrapes **book title** and **price**
- Accepts a **dynamic URL** at runtime
- Handles **pagination correctly**
- Stores data in **PostgreSQL**
- Runs Scrapy as a **one-shot job**
- Keeps the database **persistent**
- Uses **Docker Compose** for clean service separation
- Uses **Makefile** for simple developer commands

---

## 🧠 Why this project exists

Most Scrapy tutorials:
- scrape data into CSV/JSON
- run everything locally
- don’t show how real systems are structured

In real-world scraping:
- scrapers are **jobs**, not long-running services
- databases live independently
- containers are disposable
- configuration must be repeatable

`scrape2postgresql` demonstrates exactly that.

---

## 🏗 Architecture (High level)


│ Scrapy (one shot) │ ───▶ │ PostgreSQL (persistent)│


- Scrapy container:
  - starts
  - crawls
  - inserts data
  - exits cleanly

- PostgreSQL container:
  - stays running
  - persists data on host machine using Docker volume

---

## ⚙️ How it works (step-by-step)

1. PostgreSQL runs as a service container
2. Scrapy runs as a temporary container
3. A URL is passed at runtime
4. Scrapy:
   - requests the page
   - follows pagination
   - extracts structured data
   - writes rows to PostgreSQL
5. Scrapy exits
6. Database remains available for querying

---

## 🧰 Prerequisites

- Docker Desktop
- docker-compose 
- Make (preinstalled on macOS/Linux)

Verify:
```bash
docker compose version
make --version
```
---
Usage : 

🏁 Quick Start (Recommended)

1. Start PostgreSQL
```
make db
```
2. Run the scraper with a URL
```
make scrape url="https://books.toscrape.com/catalogue/category/books/business_35/index.html"
```
Scraper runs once
Data is inserted to db
Container exits automatically

3. Query the Database
```
make psql
```
then
```
SELECT title, price FROM books;
```

## Makefile commands
| Command                 | Description                 |
| ----------------------- | --------------------------- |
| `make db`               | Start PostgreSQL            |
| `make scrape url="..."` | Run scraper once            |
| `make psql`             | Open PostgreSQL shell       |
| `make logs`             | View Postgres logs          |
| `make down`             | Stop all containers         |
| `make clean`            | Stop containers + delete DB |
| `make build`            | Rebuild scraper image       |
| `make rebuild`          | Full rebuild                |
| `make reset-db`         | Clear table + reset IDs     |

--

## Useful SQL commands to query the database
```
-- View all entries
SELECT * FROM books;

-- Only title + price
SELECT title, price FROM books;

-- Count rows
SELECT COUNT(*) FROM books;

-- Reset table
TRUNCATE TABLE books RESTART IDENTITY;
```
--

## Teardown

1. Stop running containers (db) without deleting existing data
```
make down
```

2. Remove all containers and persisitent data
```
make clean
```

3. Rebuild from docker-compose
```
make rebuild
```

----

## 🔧 How to adapt this project for your own scraping needs

You can easily adapt this project to scrape other websites:
1. Change the spider logic
Edit:
```
bookscraper/bookscraper/spiders/books.py
```
Update selectors
Extract more fields
Follow detail pages

2. Change the database schema

Edit :
```
pipelines.py
```
- Add new coloumns
- Normalize data
- Add constraints 

3. Add more spiders 

Create new file under:
```
bookscraper/bookscraper/spiders/
```
Each spider can use the same database pipeline

4. Use a different website 

As long as the site structure is consistent:
- pass a new URL
- update selectors
- reuse everything else

## 🐳 Why Docker Compose?
- Consistent environments
- No local dependency issues
- Easy teardown and rebuild
- Clear separation of concerns
- Matches production workflows

## ⚠️ Disclaimer
This project is for learning and demonstration purposes only.
Always:
- check a website’s terms of service
- respect robots.txt
- scrape responsibly

## 🌱 Next improvements (ideas)
- Zyte API
- Add .env file for configuration
- Track scrape timestamps
- Store price history
- Add FastAPI to expose data
- Schedule runs via cron or CI


