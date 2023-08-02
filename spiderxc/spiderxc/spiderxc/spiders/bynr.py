import scrapy
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy import Request
import copy
from scrapy.http import HtmlResponse
from spiderxc.items import MovieItem
import re
import string
class OrdosSpider(scrapy.Spider):
    name = "bynr"
    allowed_domains = ["nmj.bynr.gov.cn"]

    def start_requests(self):
        yield scrapy.Request(url='http://nmj.bynr.gov.cn/zwdt/dfxx/index.html')
        yield scrapy.Request(url='http://nmj.bynr.gov.cn/zwdt/ywsd/index.html')
        yield scrapy.Request(url='http://nmj.bynr.gov.cn/zwdt/aqsc/index.html')
        for page in range(1, 121):
            url = f'http://nmj.bynr.gov.cn/zwdt/ywsd/index_{page}.html'
            yield scrapy.Request(url=url)
        for page in range(1, 500):
            url = f'http://nmj.bynr.gov.cn/zwdt/dfxx/index_{page}.html'
            yield scrapy.Request(url=url)
        for page in range(1,180):
            url = f'http://nmj.bynr.gov.cn/zwdt/aqsc/index_{page}.html'
            yield scrapy.Request(url=url)
    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('//*[@id="bjxToolsbar_container"]/div[3]/div[2]/div[2]/div[2]/div')

        for list_item in list_items:
            movie_item = MovieItem()
            url = list_item.xpath('./a/@href').get()
            if 'dfxx' in response.url:
                movie_item['url'] = 'http://nmj.bynr.gov.cn/zwdt/dfxx' + url[1:]
            elif 'ywsd' in response.url:
                movie_item['url'] = 'http://nmj.bynr.gov.cn/zwdt/ywsd' + url[1:]
            elif 'aqsc' in response.url:
                movie_item['url'] = 'http://nmj.bynr.gov.cn/zwdt/aqsc' + url[1:]
            movie_item['update_at'] = list_item.xpath('./a/span[2]/text()').get()
            movie_item['title'] = list_item.xpath('./a/span[1]/text()').get()
            detail_url = movie_item['url']
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = copy.deepcopy(kwargs['item'])
        list_items = response.xpath('//*[@id="bjxToolsbar_container"]/div[3]/div[3]/div[3]')
        for list_item in list_items:
            data = list_item.get()
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(data, 'html.parser')
            # 移除样式标签及其内容
            for style_tag in soup.find_all('style'):
                style_tag.extract()
            # 提取所需的文本数据
            cleaned_data = soup.get_text(strip=True)
            movie_item['data'] = cleaned_data
            yield movie_item
