import scrapy
from scrapy import Selector
from scrapy import Request
import copy
from spiderxc.items import MovieItem

class WuhaiSpider(scrapy.Spider):
    name = "wuhai"
    allowed_domains = ["nmj.wuhai.gov.cn"]

    def start_requests(self):
        keywords = ['tpgj75/ea4b87e0', '257842/ac8bfed0', '257838/727fe88d']
        for keyword in keywords:
            for page in range(1, 60):
                url = f'http://nmj.wuhai.gov.cn/nongmyj/257815/{keyword}-{page}.html'
                yield scrapy.Request(url=url)

    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('/html/body/div[5]/div/div[2]/div/div[2]/ul/li')

        for list_item in list_items:
            movie_item = MovieItem()
            url = list_item.xpath('./a/@href').get()
            movie_item['url'] = 'http://nmj.wuhai.gov.cn/' + url
            movie_item['update_at'] = list_item.xpath('./span/text()').get()
            movie_item['title'] = list_item.xpath('./a/text()').get()

            detail_url = 'http://nmj.huhhot.gov.cn/zwdt/nmdt' + url
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = copy.deepcopy(kwargs['item'])
        list_items = response.xpath('/html/body/div[3]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[3]')
        for list_item in list_items:
            data = list_item.xpath('.//p/text()').getall()
            cleaned_data = ''.join([text.replace('\u3000', '').replace('\n', '').replace('\xa0', '').strip() for text in data])
            movie_item['data'] = cleaned_data
            yield movie_item
