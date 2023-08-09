import scrapy
from scrapy import Selector
from scrapy import Request
import copy
from scrapy.http import HtmlResponse
from spiderxc.items import MovieItem
import re

class TongliaoSpider(scrapy.Spider):
    name = "tongliao"
    allowed_domains = ["nmj.tongliao.gov.cn"]

    def start_requests(self):
        yield scrapy.Request(url='https://nmj.tongliao.gov.cn/nmyj/qxdt/list.shtml')
        yield scrapy.Request(url='https://nmj.tongliao.gov.cn/nmyj/nmydt/list.shtml')
        for page in range(2, 250):
            url = f'https://nmj.tongliao.gov.cn/nmyj/qxdt/list_{page}.shtml'
            yield scrapy.Request(url=url)
        for page in range(2,81):
            url = f'https://nmj.tongliao.gov.cn/nmyj/nmydt/list_{page}.shtml'
            yield scrapy.Request(url=url)


    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('/html/body/div[2]/div[3]/ul/li')

        for list_item in list_items:
            movie_item = MovieItem()
            url = list_item.xpath('./a/@href').get()
            movie_item['url'] = 'https://nmj.tongliao.gov.cn' + url
            movie_item['update_at'] = list_item.xpath('./span/text()').get()
            movie_item['title'] = list_item.xpath('./a/text()').get()
            detail_url = 'https://nmj.tongliao.gov.cn' + url
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = copy.deepcopy(kwargs['item'])
        list_items = response.xpath('//*[@class="pages_content"]')
        for list_item in list_items:
            data = list_item.xpath('.//p//text()').getall()
            cleaned_data = ''.join([text.replace('\u3000', '').replace('\n', '').replace('\xa0', '').strip() for text in data])
            movie_item['data'] = cleaned_data
            yield movie_item
