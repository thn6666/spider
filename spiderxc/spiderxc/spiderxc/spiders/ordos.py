import scrapy
from scrapy import Selector
from scrapy import Request
import copy
from scrapy.http import HtmlResponse
from spiderxc.items import MovieItem
import re

class OrdosSpider(scrapy.Spider):
    name = "ordos"
    allowed_domains = ["nmj.ordos.gov.cn"]

    def start_requests(self):
        yield scrapy.Request(url='http://nmj.ordos.gov.cn/xwdt/bmdt/index.html')
        yield scrapy.Request(url='http://nmj.ordos.gov.cn/xwdt/qqdt/index.html')
        yield scrapy.Request(url='http://nmj.ordos.gov.cn/xwdt/tzgg/index.html')
        for page in range(1, 49):
            url = f'http://nmj.ordos.gov.cn/xwdt/qqdt/index_{page}.html'
            yield scrapy.Request(url=url)
        for page in range(1, 49):
            url = f'http://nmj.ordos.gov.cn/xwdt/bmdt/index_49.html'
            yield scrapy.Request(url=url)
        for page in range(1,31):
            url = f'http://nmj.ordos.gov.cn/xwdt/tzgg/index_{page}.html'
            yield scrapy.Request(url=url)
    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/ul/li')

        for list_item in list_items:
            movie_item = MovieItem()
            url = list_item.xpath('./a/@href').get()
            if 'tzgg' in response.url:
                movie_item['url'] = 'http://nmj.ordos.gov.cn/xwdt/tzgg' + url[1:]
            elif 'bmdt' in response.url:
                movie_item['url'] = 'http://nmj.ordos.gov.cn/xwdt/bmdt' + url[1:]
            elif 'qqdt' in response.url:
                movie_item['url'] = 'http://nmj.ordos.gov.cn/xwdt/qqdt' + url[1:]
            movie_item['update_at'] = list_item.xpath('./a/span/text()').get()
            movie_item['title'] = list_item.xpath('./a/p/text()').get()
            detail_url = movie_item['url']
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = copy.deepcopy(kwargs['item'])
        list_items = response.xpath('//*[@id="xxcb_content"]')
        for list_item in list_items:
            data = list_item.xpath('.//p//text()').getall()
            cleaned_data = ''.join([text.replace('\u3000', '').replace('\n', '').replace('\xa0', '').strip() for text in data])
            movie_item['data'] = cleaned_data
            yield movie_item
