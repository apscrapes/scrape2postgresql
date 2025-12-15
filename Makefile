PROJECT_NAME=books
POSTGRES_CONTAINER=books_postgres
SCRAPER_CONTAINER=books_scraper

# Start ONLY the Postgres database 
db:
	docker compose up -d postgres

# Run the Scrapy spider once (container exits after crawling)
scrape:
	docker compose run --rm -e URL="$(url)" scrapy

# View logs for Postgres
logs:
	docker logs -f $(POSTGRES_CONTAINER)

# Enter PostgreSQL shell
psql:
	docker exec -it $(POSTGRES_CONTAINER) psql -U user -d books_db

# Stop all containers
down:
	docker compose down

# Stop and remove docker volumes (to get a fresh DB)
clean:
	docker compose down -v

# Rebuild scraper image
build:
	docker compose build scrapy

# Rebuild EVERYTHING
rebuild:
	docker compose down -v
	docker compose build
