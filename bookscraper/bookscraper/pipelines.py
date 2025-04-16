import sys
import os
from itemadapter import ItemAdapter

# Replace with your actual path to the mysql-connector-python directory
mysql_path = r"C:/Users/Kasparov/Desktop/datasets/venv/Lib/site-packages/mysql/connector/__init__.py"

if os.path.exists(mysql_path):
    sys.path.insert(0, mysql_path)

import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='', database='books')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS books(id INT AUTO_INCREMENT PRIMARY KEY, title TEXT, price DECIMAL, rating INT, category VARCHAR(255), descrip TEXT, book_type VARCHAR(255))")
conn.commit()

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price = adapter.get("price")
        if price:
            adapter["price"] = float(price.replace('£', ''))

        rating = adapter.get('rating')
        if rating:
            rating_parts = rating.split(' ')
            if len(rating_parts) > 1:
                rating_value = rating_parts[1].lower()
                rating_map = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
                adapter['rating'] = rating_map.get(rating_value, 0)
        return item

class SaveToMySqlMyPipeline:
    def process_item(self, item, spider):
        cur.execute("INSERT INTO books(title, price, rating, category, descrip, book_type) VALUES (%s, %s, %s, %s, %s, %s)", (item["title"], item["price"], item["rating"], item["category"], item["descrip"], item["book_type"][0]))
        conn.commit()
        return item

def close_spider(spider):
    cur.close()
    conn.close()