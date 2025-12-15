# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import os

class BookscraperPipeline:
    def process_item(self, item, spider):
        return item

class PostgresPipeline:

    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT,
            price TEXT,
            scraped_at TIMESTAMP DEFAULT NOW()
        );
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        self.cur.execute(
            "INSERT INTO books (title, price) VALUES (%s, %s)",
            (item["title"], item["price"])
        )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
