# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy import signals
from spiderxc.settings import USER_AGENTS
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# def get_cookies_dict():
#     cookies_str = 'COLLCK=514720654; JSESSIONID=AEDA13D7B1CC85AAFF4FB98763A1680D; TS0171726e=01dde16a1e0e599768b314b7ba67a94b5fc3972fb4d58b67dea0d38a0c1373a3245c9a1de61b5e6f01e3e135cab7d9e5643caaa941; _trs_uv=l9soc0sj_5296_k73l; _trs_ua_s_1=lkrphd3n_5305_74xk; TS01708977=01dde16a1e0e599768b314b7ba67a94b5fc3972fb4d58b67dea0d38a0c1373a3245c9a1de61b5e6f01e3e135cab7d9e5643caaa941'
#     cookies_dict = {}
#     for item in cookies_str.split('; '):
#         key, value = item.split('=', maxsplit=1)
#         cookies_dict[key] = value
#         return cookies_dict
# COOKIES_DICT = get_cookies_dict()
class SpiderxcSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SpiderxcDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        request.cookies = {

        }
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # request.cookies = COOKIES_DICT
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    class RandomUserAgentMiddleware:
        def process_request(self, request, spider):
            # 随机选择一个User-Agent并设置到请求头中
            user_agent = random.choice(USER_AGENTS)
            request.headers['User-Agent'] = user_agent