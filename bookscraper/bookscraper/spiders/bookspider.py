import scrapy
from bookscraper.items import BookItem
import random

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    custom_settings = {
        'FEEDS': {
            'bookdata.json': {'format': 'json', 'overwrite': True},
        }
    }

    USER_AGENTS = [
    # Chrome User Agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",

    # Firefox User Agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0",


    # Mobile User Agents
    "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
]


    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            book_url = book.css('h3 a').attrib['href']
            if book_url is not None:
                if 'catalogue/' in book_url:
                    book_full_url = 'https://books.toscrape.com/' + book_url
                else:
                    book_full_url = 'https://books.toscrape.com/catalogue/' + book_url

                yield response.follow(book_full_url, callback = self.parseBook)


        next_page = response.css('li.next a').attrib['href']
        if next_page is not None:
            if 'catalogue/' in next_page:
                 next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page

            yield response.follow(next_page_url, callback = self.parse)
    
    def parseBook(self,response): 
        table_rows = response.css('table tr')
        book_item = BookItem()


        
        book_item['title'] = response.css('.product_main h1::text').get()
        book_item['price'] = response.css('.product_main .price_color::text').get()
        book_item['rating'] =  response.css('.product_main .star-rating').attrib['class']
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['descrip'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book_item['book_type'] = table_rows[1].css('td::text').get()


        yield book_item
        
            


