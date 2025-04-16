# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


def serialize_price(value):
    value = str(value)
    return f'€ {value}'

class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    category = scrapy.Field()
    descrip = scrapy.Field()
    book_type = scrapy.Field()