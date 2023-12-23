import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule 
from myspider.items import MyspiderItem


class ImagesSpider(CrawlSpider):
    name = "images"
    # allowed_domains = ["", ""]
    start_urls = ["https://arxiv.org/list/cs.AI/recent"]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=(r"/ist/cs.AI/",), )),
        # Rule(LinkExtractor(allow=(r"/archive/",), )),
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=(r"abs/[0-9]{4}.[0-9]{5}",)), callback="parse_item", follow=True),

        )

    def parse_item(self, response):
        file_url = response.css('div.full-text').css('a.abs-button.download-pdf::attr(href)').get()
        # print(f"file_url is {file_url}") 
        file_url = response.urljoin(file_url) 
        
        file_extension = file_url.split('.')[-1] 
        if file_extension not in ('pdf'): 
            return
        item = MyspiderItem() 
        item['file_urls'] = [file_url] 
        item['original_file_name'] = file_url.split('/')[-1] 
        yield item 