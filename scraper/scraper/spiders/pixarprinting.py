import scrapy


class PixarprintingSpider(scrapy.Spider):
    name = "pixarprinting"
   
    allowed_domains = ["pixartprinting.fr"]
    start_urls = ["https://pixartprinting.fr/petit-format/enveloppes/enveloppes-commerciales/"]


# prod-title
    def parse(self, response):
       title = response.css(".prod-title::text").get()
       yield {
        'title':title
       }
    
