import scrapy,json
from scrapy.loader import ItemLoader
from snkrs.items import SnkrsItem

class QuotesSpider(scrapy.Spider):
    name = "snkrs"


    def start_requests(self):
        self.count = 0
        baseurl='https://api.nike.com/snkrs/content/v1/?&country=US&language=en&offset={PN}&orderBy=published'
        for i in range(0,2558,50):
            yield scrapy.Request(url=baseurl.replace('{PN}',str(i)), callback=self.parse)


    def parse(self, response):
        l = ItemLoader(item=SnkrsItem(), response=response)
        data=json.loads(response.body)
        for d in data['threads']:
            l.add_value('shoe', d)
            self.count+=1
            yield l.load_item()