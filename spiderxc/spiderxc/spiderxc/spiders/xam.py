
import scrapy
from scrapy import Selector
from scrapy import Request
import copy
from scrapy.http import HtmlResponse
from spiderxc.items import MovieItem
import re
# headers = {
#     "user-agent": "PostmanRuntime-ApipostRuntime/1.1.0",
#     "cookie": "COLLCK=514720654; JSESSIONID=AEDA13D7B1CC85AAFF4FB98763A1680D; TS0171726e=01dde16a1e0e599768b314b7ba67a94b5fc3972fb4d58b67dea0d38a0c1373a3245c9a1de61b5e6f01e3e135cab7d9e5643caaa941; _trs_uv=l9soc0sj_5296_k73l; _trs_ua_s_1=lkrphd3n_5305_74xk; TS01708977=01dde16a1e2c0a040f92c0ee075a8b0c62cfda5af4c696a7e2b5633ce8a739b1df58ccc725bc3e30f0a2a0e5f9089f0270b9a44239",
# }
class HuhhotSpider(scrapy.Spider):
    name = "xam"
    allowed_domains = ["nmj.xam.gov.cn"]

    def start_requests(self):
        for page in range(1, 41):
            url = f'http://nmj.xam.gov.cn/xamagri/1023721/1023756/1023713/37994696-{page}.html'
            yield scrapy.Request(url=url)
        for page in range(1,201):
            url = f'http://nmj.xam.gov.cn/xamagri/1023721/1023756/1023759/f04a2c59-{page}.html'
            yield scrapy.Request(url=url)
        for page in range(1,214):
            url = f'http://nmj.xam.gov.cn/xamagri/1023721/1023756/qxdt84/56061db6-{page}.html'
            yield scrapy.Request(url=url)

    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('//*[@class="zd_mod2_main"]/ul/li')

        for list_item in list_items:
            movie_item = MovieItem()
            url = list_item.xpath('./span[1]/a/@href').get()
            movie_item['url'] = 'http://nmj.xam.gov.cn' + url
            movie_item['update_at'] = list_item.xpath('./span[2]/text()').get()
            movie_item['title'] = list_item.xpath('./span[1]/a/text()').get().strip()
            detail_url = movie_item['url']
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = copy.deepcopy(kwargs['item'])
        list_items = response.xpath('//*[@id="zoom"]')
        for list_item in list_items:
            data = list_item.xpath('.//text()').getall()
            cleaned_data = ''.join([text.replace('\u3000', '').replace('\n', '').replace('\xa0', '').replace('\u2000', '').strip() for text in data])
            movie_item['data'] = cleaned_data
            yield movie_item
