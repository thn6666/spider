import scrapy
from scrapy import Selector
from scrapy import Request
import copy
from spiderxc.items import MovieItem
headers = {
    "user-agent": "PostmanRuntime-ApipostRuntime/1.1.0",
    "cookie": "JSESSIONID=121BF86B188D06D29483619B6C4E0F5F; _gscu_1475204090=88194628joihot27; UM_distinctid=189103dbc6da9b-00731feba4ce5a-26031d51-144000-189103dbc6e14ac; _gscbrs_1475204090=1; CNZZDATA1281108930=71023178-1688194628-%7C1690890479; _gscs_1475204090=90889126pghcxv75|pv:22",
}
class WuhaiSpider(scrapy.Spider):
    name = "wuhai"
    allowed_domains = ["nmj.wuhai.gov.cn"]

    def start_requests(self):
        for page in range(1,61):
            url = f'http://nmj.wuhai.gov.cn/nongmyj/257815/257838/727fe88d-{page}.html'
            yield scrapy.Request(url=url)
        for page in range(1,11):
            url = f'http://nmj.wuhai.gov.cn/nongmyj/257815/257842/ac8bfed0-{page}.html'
            yield scrapy.Request(url=url)
        for page in range(1,26):
            url = f'http://nmj.wuhai.gov.cn/nongmyj/257815/tpgj75/ea4b87e0-{page}.html'
            yield scrapy.Request(url=url)
    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('//*[@class="portlet"]/div[2]/ul/li')

        for list_item in list_items:
            movie_item = MovieItem()
            url = list_item.xpath('./a/@href').get()
            movie_item['url'] = 'http://nmj.wuhai.gov.cn/' + url
            movie_item['update_at'] = list_item.xpath('./span/text()').get()
            movie_item['title'] = list_item.xpath('./a/text()').get()
            detail_url = movie_item['url']
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = copy.deepcopy(kwargs['item'])
        list_items = response.xpath('//*[@id="zoom"]')
        for list_item in list_items:
            data = list_item.xpath('.//text()').getall()
            cleaned_data = ''.join([text.replace('\u3000', '').replace('\n', '').replace('\xa0', '').strip() for text in data])
            movie_item['data'] = cleaned_data
            yield movie_item
