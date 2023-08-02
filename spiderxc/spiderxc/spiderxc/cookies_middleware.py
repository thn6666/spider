
class CookieMiddleware:
    def process_request(self, request, spider):
        # 在这里根据spider的名称或请求的URL设置不同的Cookie
        if spider.name == 'chifeng':
            request.headers['Cookie'] = 'chifeng_cookie=value1'
        elif spider.name == 'wuhai':
            request.headers['Cookie'] = 'wuhai_cookie=value2'
        # 还可以根据请求的URL等其他条件设置不同的Cookie
