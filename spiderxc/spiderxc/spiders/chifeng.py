import scrapy
from scrapy import Selector
from scrapy import Request
import copy
from scrapy.http import HtmlResponse
from spiderxc.items import MovieItem
import re

class HuhhotSpider(scrapy.Spider):
    name = "chifeng"
    allowed_domains = ["nmj.chifeng.gov.cn"]

    def start_requests(self):
        yield scrapy.Request(url='http://nmj.chifeng.gov.cn/zwxx/sndt/sjdt/index.html')
        yield scrapy.Request(url='http://nmj.chifeng.gov.cn/zwxx/sndt/qxdt/index.html')
        keywords = ['sjdt','qxdt']
        for keyword in keywords:
            for page in range(1, 7):
                url = f'http://nmj.chifeng.gov.cn/zwxx/sndt/{keyword}/index_{page}.html'
                yield scrapy.Request(url=url)

    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('//*[@id="lb"]/li')

        for list_item in list_items:
            movie_item = MovieItem()
            url = list_item.xpath('.//a/@href').get()
            if 'sjdt' in response.url:
                movie_item['url'] = 'http://nmj.chifeng.gov.cn/zwxx/sndt/sjdt' + url[1:]
            elif 'qxdt' in response.url:
                movie_item['url'] = 'http://nmj.chifeng.gov.cn/zwxx/sndt/qxdt' + url[1:]
            movie_item['update_at'] = list_item.xpath('./span/text()').get()
            movie_item['title'] = list_item.xpath('./a/text()').get()
            detail_url = movie_item['url']
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = copy.deepcopy(kwargs['item'])
        list_items = response.xpath('//*[@id="centerFont"]/div')
        for list_item in list_items:
            data = list_item.xpath('./p//text()').getall()
            cleaned_data = ''.join([text.replace('\u3000', '').replace('\n', '').replace('\xa0', '').strip() for text in data])
            movie_item['data'] = cleaned_data
            yield movie_item
