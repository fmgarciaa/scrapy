from gc import callbacks
import scrapy

# Title = //h1/a/text() 
# Quotes = //span[@class="text" and @itemprop="text"]/text()
# Top ten tagas = //span[@class="tag-item"]/a/text()
# Next page button = //ul[@class="pager"]//li[@class="next"]/a/@href

class QuotesSpider(scrapy.Spider):
    """
    How to save informatio from spider the command is:
    
    scrapy crawl <name of spider> -o <name of file.(csv, json,etc)>
    
    or we use custom_settings dictionary  how vairable
    
    """
    
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/',
    ]
    
    custom_settings = {
        'FEED_URI':'quotes.json',
        'FEED_FORMAT': 'json'
        }
    
    def parse(self, response):
        
        title = response.xpath('//h1/a/text()').get()        
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()            
        top_ten_tags = response.xpath('//span[@class="tag-item"]/a/text()').getall()

        yield {
            'title':title,
            'quotes': quotes,
            'top_ten_tags': top_ten_tags
        }
        
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse)
    