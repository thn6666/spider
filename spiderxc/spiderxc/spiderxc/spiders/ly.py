from spiderxc.items import MovieItem
import time
import re
import scrapy
from scrapy import Request
from scrapy.selector import Selector

class LySpider(scrapy.Spider):
    name = "ly"
    allowed_domains = ["nync.ly.gov.cn"]
    def start_requests(self):
        keywords =['b82d21df35219bb95f049d5131e6ecc2', '93b7e96c4fe8bdfa7fa6b69cf583c1d5']
        for keyword in keywords:
            for page in range(1,9):
                url = f'http://nync.ly.gov.cn/news.php?page={page}&NodeId={keyword}'
                yield Request(url=url)


    def parse(self, response, **kwargs):
        sel = Selector(response)

        list_items = response.xpath('/html/body/div[5]/div/table/tbody/tr')

        for list_item in list_items:
            movie_item = MovieItem()
            movie_item['url'] = 'http://nync.ly.gov.cn/' + list_item.xpath('./td[2]/a/@href').get()
            movie_item['title'] = list_item.xpath('./td[2]/a/@title').get()
            movie_item['update_at'] = list_item.xpath('./td[3]/text()').get()
            yield movie_item
