import scrapy
from urllib.parse import urljoin


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]

    def __init__(self, url=None, max_pages=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not url:
            raise ValueError("ERROR: You must pass a URL: scrapy crawl books -a url=...")

        # BooksToScrape website's pagination breaks unless URL begins
        if "/catalogue/" not in url:
            url = url.replace(
                "https://books.toscrape.com/",
                "https://books.toscrape.com/catalogue/"
            )

        self.start_urls = [url]

        # optional add a limit on number of pages to scrapee
        self.max_pages = int(max_pages) if max_pages else None
        self.pages_scraped = 0

    def parse(self, response):
        # Extract books
        for book in response.css("article.product_pod"):
            title = book.css("h3 a::attr(title)").get()
            price = book.css("p.price_color::text").get()

            yield {
                "title": title,
                "price": price,
            }

        # count pages scraped
        self.pages_scraped += 1

        # stop after max_pages
        if self.max_pages and self.pages_scraped >= self.max_pages:
            return

        # Resolve next-page relative URLs
        next_page = response.css("li.next a::attr(href)").get()

        if next_page:
            # urljoin ensures correct full path under /catalogue/
            next_page_url = urljoin(response.url, next_page)

            # follow next page in category
            yield scrapy.Request(url=next_page_url, callback=self.parse)
