import scrapy
from scrapy import Selector
from scrapy import Request
import copy
from scrapy.http import HtmlResponse
from spiderxc.items import MovieItem
import re

class HuhhotSpider(scrapy.Spider):
    name = "huhhot"
    allowed_domains = ["nmj.huhhot.gov.cn"]

    def start_requests(self):
        yield scrapy.Request(url='http://nmj.huhhot.gov.cn/zwdt/nmdt/index.html')
        for page in range(1, 41):
            url = f'http://nmj.huhhot.gov.cn/zwdt/nmdt/index_{page}.html'
            yield scrapy.Request(url=url)

    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('/html/body/div[3]/div/div[2]/ul/li')

        for list_item in list_items:
            movie_item = MovieItem()
            url = list_item.xpath('./div[2]/a/@href').get()
            movie_item['url'] = 'http://nmj.huhhot.gov.cn/zwdt/nmdt' + url[1:]
            movie_item['update_at'] = list_item.xpath('./div[1]/i/text()').get() + '-' + list_item.xpath('./div[1]/span/text()').get()
            movie_item['title'] = list_item.xpath('./div[2]/a/text()').get()
            detail_url = 'http://nmj.huhhot.gov.cn/zwdt/nmdt' + url[1:]
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = copy.deepcopy(kwargs['item'])
        list_items = response.xpath('//*[@id="pare"]')
        for list_item in list_items:
            data = list_item.xpath('./div[1]//text()').getall()
            cleaned_data = ''.join([text.replace('\u3000', '').replace('\n', '').replace('\xa0', '').strip() for text in data])
            movie_item['data'] = cleaned_data
            yield movie_item
