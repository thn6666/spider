import scrapy
from scrapy import Selector
from scrapy import Request
import copy
from scrapy.http import HtmlResponse
from spiderxc.items import MovieItem
import re

class HlbeSpider(scrapy.Spider):
    name = "hlbe"
    allowed_domains = ["nmj.hlbe.gov.cn"]

    def start_requests(self):
        for page in range(1, 171):
            url = f'http://nmj.hlbe.gov.cn/News/showList/2088/page_{page}.html'
            yield scrapy.Request(url=url)
        for page in range(1, 11):
            url = f'http://nmj.hlbe.gov.cn/News/showList/2069/page_{page}.html'
            yield scrapy.Request(url=url)
        for page in range(1,12):
            url = f'http://nmj.hlbe.gov.cn/News/showList/2089/page_{page}.html'
        for page in range(1, 301):
            url = f'http://nmj.hlbe.gov.cn/News/showList/2101/page_{page}.html'
            yield scrapy.Request(url=url)
    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('/html/body/div[3]/div/div/section[2]/div/div[2]/ul/li')

        for list_item in list_items:
            movie_item = MovieItem()
            url = list_item.xpath('./a/@href').get()
            movie_item['url'] = 'http://nmj.hlbe.gov.cn' + url
            movie_item['update_at'] = list_item.xpath('./span/text()').get()
            movie_item['title'] = list_item.xpath('./a/text()').get()
            detail_url = movie_item['url']
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = copy.deepcopy(kwargs['item'])
        list_items = response.xpath('//*[@id="zoom"]')
        for list_item in list_items:
            data = list_item.xpath('.//p//text()').getall()
            cleaned_data = ''.join([text.replace('\u3000', '').replace('\n', '').replace('\xa0', '').strip() for text in data])
            movie_item['data'] = cleaned_data
            yield movie_item
