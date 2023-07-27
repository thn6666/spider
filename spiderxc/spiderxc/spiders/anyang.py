import scrapy
from scrapy import Selector
from scrapy import Request
from scrapy.http import HtmlResponse
from spiderxc.items import MovieItem
import re
import copy


class AnyangSpider(scrapy.Spider):
    name = "anyang"
    allowed_domains = ["nyj.anyang.gov.cn"]

    def start_requests(self):
        keywords = ['ayny', 'tzgg']
        pags = ['_1', '', '_2', '_3', '_4']
        for keyword in keywords:
            for pag in pags:
                url = f'https://nyj.anyang.gov.cn/ywdt/{keyword}/index{pag}.html'
                yield scrapy.Request(url=url)

    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('/html/body/div[2]/div/div[3]/div/ul/li')

        for list_item in list_items:
            movie_item = MovieItem()
            movie_item['url'] = list_item.xpath('./a/@href').get()
            movie_item['update_at'] = list_item.xpath('./span/text()').get()
            movie_item['title'] = list_item.xpath('./a/@title').get()

            detail_url = list_item.xpath('./a/@href').get()
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': copy.deepcopy(movie_item)})

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = kwargs['item']
        list_items = response.xpath('//*[@id="zoom"]')
        for list_item in list_items:
            data = list_item.xpath('.//p/text()').getall()
            cleaned_data = ''.join([text.replace('\u3000', '').replace('\n', '').replace('\xa0', '') for text in data])
            movie_item['data'] = cleaned_data
            yield movie_item
