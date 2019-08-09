# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import shelve

import requests

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy_splash import SplashRequest


class MaigooSpiderMiddleware(object):
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


class MaigooDownloaderMiddleware(object):
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
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
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
        spider.logger.info('Spider opened: %s' % spider.name)



import random
class GfUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agents=crawler.settings.get('USER_AGENTS')
        )

    def process_request(self, request, spider):
        # print('agent-----%s' %agent)
        request.headers['User-Agent'] = random.choice(self.user_agents)



##代理ip 2.0
class SplashProxyPoolsMiddleware(object):
    '''
    设置Proxy
    '''
    proxydict=dict()
    def __init__(self, proxyapi,ipdbs,proxydefault):
        self.proxyapi=proxyapi
        self.ipdbs=ipdbs
        self.ip=proxydefault

    @classmethod
    def from_crawler(cls, crawler):
        proxyapi = crawler.settings.get('PROXYAPI')
        ipdbs = crawler.settings.get("IPDBS")
        proxydefault=crawler.settings.get('PROXY_DEFAULT')
        s = cls(proxyapi, ipdbs,proxydefault)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        # print(f"request ip:{self.ip}")
        if isinstance(request, SplashRequest):
            request.meta['splash']['args']['proxy'] =self.ip
        else:
            request.meta['proxy']=self.ip

        # "180.164.24.165:53281"
        # request.meta['proxy']="http://180.164.24.165:53281"

    def process_response(self, request, response, spider):

        if isinstance(request, SplashRequest):
            ip = request.meta['splash']['args']['proxy']
        else:
            ip = request.meta.get('proxy',None)

        if 300 > response.status >= 200:
            # print(f"process_response = 200:{response.status==200}")
            # print(f"proxy ip:{ip}")
            if ip:self.proxydict.get("usefulips",[]).append(ip)
            return response
        else:
            if ip:self.proxydict.get("nousefulips", []).append(ip)
            # with open("ProxyPoolsMiddleware_tmp.html","wb") as f:
            #     f.write(response.body)
            self.update_proxyip()
            return request
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # return response
    def process_exception(self,request,exception,spider):
        if isinstance(request, SplashRequest):
            ip = request.meta.get('splash', {}).get('args', {}).get('proxy')
        else:
            ip = request.meta.get('proxy')
        if ip:
            self.proxydict.get("nousefulips", []).append(ip)
        self.update_proxyip()
        return request

    def update_proxyip(self):
        ip = requests.request(method="GET", url=self.proxyapi + "/get").text
        if len(ip)<3:ip=self.proxydefault
        self.ip="http://"+ip

    def spider_closed(self):
        with shelve.open(self.ipdbs) as f:
            tmp=f.get('ipdbs',[])
            tmp.append(self.proxydict)
            f['ipdbs']=tmp


from scrapy.core.downloader.handlers import http11
from twisted.internet import error

##代理ip 固定ip代理
class SplashOneProxyPoolMiddleware(object):
    '''
    设置Proxy
    '''
    proxydict=dict()
    def __init__(self, proxydefault):
        self.proxydefault=proxydefault

    @classmethod
    def from_crawler(cls, crawler):
        proxydefault=crawler.settings.get('PROXY_DEFAULT')
        s = cls(proxydefault)
        return s

    def process_request(self, request, spider):
        if isinstance(request,SplashRequest):
            request._splash_args.update({'proxy':self.proxydefault})
        else:
            request.meta['proxy'] = self.proxydefault


    def process_response(self, request, response, spider):
        return response

    def process_exception(self,request,exception,spider):
        if isinstance(request, SplashRequest):
            ip = request._splash_args.get('proxy')
        else:
            ip = request.meta.get('proxy')
        if not ip:
            if isinstance(exception,(error.TimeoutError,http11.TunnelError)):
                return request
