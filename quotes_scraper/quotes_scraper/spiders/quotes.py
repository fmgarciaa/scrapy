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
    
    """Spider with super powers

    custom_settings = {}
    Allow us add super powers to our spider with some arguments previously
    charge in scrapy.
    """
    
    custom_settings = {
        'FEED_URI':'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24, # total of request on server that our spider will do
        'MEMUSAGE_LIMIT_MB' : 2048, # ram memory that our spider will use
        'MEMUSAGE_NOTIFY_EMAIL': ['me@gmail.com'], # mail that our spider notify when the ram memory is out
        'ROBOTSTXT_OBEY' : True, # if we want that our spider obey the robots.txt file from where I want do scrapping
        'USER_AGENT': 'any other name', # the name that our spider will use when try to connect with server
        'FEED_EXPORT_ENCODING': 'utf-8' # character format we want our spider to use to store the data
        }
    
    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes})   
        else:
            yield {
                'quotes': quotes
            }
            
            
    def parse(self, response):
        
        title = response.xpath('//h1/a/text()').get()        
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()            
        top_tags = response.xpath('//span[@class="tag-item"]/a/text()').getall()

        
        """pass an argument to scrapy
        When run our spider we can pass an argument with flag. It would look like this: 
        scrapy crawl quotes -a <variable>=<argument>
        In this case I set a variable with name top
        that bring me the tags that I put on variable.            
        """
        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        
        yield {
            'title':title,
            'top_tags': top_tags
        }
                
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes})
    