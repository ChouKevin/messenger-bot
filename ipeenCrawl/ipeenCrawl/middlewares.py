# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
from scrapy import signals

log = logging.getLogger('scrapy.proxy')

class IpeencrawlSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

import logging
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)

class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        fallback = crawler.settings.get('FAKEUSERAGENT_FALLBACK', None)
        self.ua = UserAgent(fallback=fallback)
        self.per_proxy = crawler.settings.get('RANDOM_UA_PER_PROXY', False)
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
        self.proxy2ua = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)
        
        if self.per_proxy:
            proxy = request.meta.get('proxy')
            if proxy not in self.proxy2ua:
                self.proxy2ua[proxy] = get_ua()
                # logging.debug('Assign User-Agent %s to Proxy %s'
                #              % (self.proxy2ua[proxy], proxy))
            request.headers.setdefault('User-Agent', self.proxy2ua[proxy])
        else:
            request.headers.setdefault('User-Agent', get_ua())


import json, time, os, random, re
from threading import Timer

class ProxyMiddleware(object):
    def __init__(self, proxy = ""):
        super(ProxyMiddleware, self).__init__()
        self.proxy = proxy

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings['HTTP_PROXY'])
    
    def process_request(self, request, spider):
        if self.proxy :
            log.info('Use proxy : {0}'.format(self.proxy))
            request.meta['proxy'] = self.proxy
    # def process_request(self, request, spider):
    #     if self.reload_proxy:
    #         self.load_proxy()
    #         Timer(600, self.load_proxy, ()).start()
    #     if 'proxy' in request.meta:
    #         if request.meta["exception"] is False:
    #             return
    #     request.meta["exception"] = False
    #     if self.proxy_list:
    #         request.meta['proxy'] = random.choice(self.proxy_list)

    # def process_response(self, request, response, spider):
    #     if response.status in [403, 400] and 'proxy' in request.meta:
    #         log.info('Response status: {0} using proxy {1} retrying request to {2}'.format(response.status, \
    #             request.meta['proxy'], request.url))
    #         self.delete_proxy(request.meta['proxy'])
    #         del request.meta['proxy']
    #         return request
    #     return response

    # def process_exception(self, request, exception, spider):
    #     if 'proxy' in request.meta:
    #         self.delete_proxy(request.meta['proxy'])
    #         del request.meta['proxy']
    #         request.meta["exception"] = True
    #     else:
    #         return
    # def load_proxy(self, path=""):
    #     self.reload_proxy = not self.reload_proxy
    #     with open(os.path.join(path, 'proxyList.txt'), 'r') as read_file:
    #         self.json_to_str(json.load(read_file))

    # def json_to_str(self, data):
    #     for item in data:
    #         proxy = ''
    #         if not item['https'] or item['level'] != 'transparent':
    #             proxy = 'https://'
    #         else: proxy = 'http://'
    #         self.proxy_list.append(proxy + item['ip'] + ':' + item['port'])

    # def delete_proxy(self, data):
    #     ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}?', data)[0]
    #     port = re.findall(r'[0-9]+(?:\.[0-9]+){3}:([0-9]+)?', data)[0]
    #     try:
    #         self.proxy_list.remove(ip + ':' + port)
    #         log.info('Removing failed proxy <{0}>, {1} proxies left'.format(ip + ':' + port, len(self.proxy_list)))
    #     except :
    #         pass
