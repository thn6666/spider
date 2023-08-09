import scrapy
from scrapy import Selector
from scrapy import Request
import copy
from spiderxc.items import MovieItem
class BaotouSpider(scrapy.Spider):
    name = "baotou"
    allowed_domains = ["nmj.baotou.gov.cn"]

    def start_requests(self):
        keywords = ['zwdt','qxdt','tzgg']
        for key in keywords:
            for page in range(1,324):
                url = f'http://nmj.baotou.gov.cn/{key}_{page}.jhtml'
                yield scrapy.Request(url=url)

    def parse(self, response):
        sel = Selector(response)
        list_items = response.xpath('//div[@class="scy_lbsj-right-nr"]/ul/li')

        for list_item in list_items:
            movie_item = MovieItem()
            url = list_item.xpath('./a/@href').get()
            movie_item['url'] = 'http://nmj.baotou.gov.cn' + url
            movie_item['update_at'] = list_item.xpath('./span/text()').get()
            movie_item['title'] = list_item.xpath('./a/text()').get()
            detail_url = 'http://nmj.baotou.gov.cn' + url

            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})


    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = copy.deepcopy(kwargs['item'])
        if 'tzgg' in response.url:
            list_items = response.xpath('//*[@class="wenzhang"]')
            for list_item in list_items:
                data = list_item.xpath('.//text()').getall()
                cleaned_data = ''.join(
                    [text.replace('\u3000', '').replace('\n', '').replace('\xa0', '').strip() for text in data])
                movie_item['data'] = cleaned_data
                yield movie_item
        else:
            list_items = response.xpath('//*[@id="content_body"]')
            for list_item in list_items:
                data = list_item.xpath('./div[2]//text()').getall()
                cleaned_data = ''.join([text.replace('\u3000', '').replace('\n', '').replace('\xa0', '').strip() for text in data])
                movie_item['data'] = cleaned_data
                yield movie_item
