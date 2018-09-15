import scrapy,json
from scrapy.loader import ItemLoader
from snkrs.items import SnkrsItem

class QuotesSpider(scrapy.Spider):
    name = "snkrs"


    def start_requests(self):
        self.count = 0
        baseurl='https://api.nike.com/snkrs/content/v1/?&country=US&language=en&offset={PN}&orderBy=published'
        for i in range(0,2600,50):
            yield scrapy.Request(url=baseurl.replace('{PN}',str(i)), callback=self.parse,dont_filter=True)


    def parse(self, response):
        print(response)

        data=json.loads(response.body)
        for d in data['threads']:
            l = ItemLoader(item=SnkrsItem(), response=response)
            l.add_value('shoe', d)
            self.count+=1
            yield l.load_item()