#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author : shaw
# @Site : 
# @File : testproxy.py
# @Time : 2019/8/9 10:44
# @Software: PyCharm
from datetime import datetime

import scrapy
from scrapy_splash import SplashRequest


lua_source='''
function main(splash, args)
      assert(splash:wait(0.5))
      splash:set_custom_headers({
        ['Accept'] = '*/*',
        ['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        ['Cache-Control'] = 'max-age=0',
        ['Connection'] = 'keep-alive',
        ['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
      })
      splash.private_mode_enabled = false
      splash:go(args.url)
      assert(splash:wait(3))

      return {
        html = splash:html()
      }
end
'''

class TestproxySpider(scrapy.Spider):
    name = 'testip'
    # allowed_domains = ['ip.cn']
    # start_urls = ['https://ip.cn']

    custom_settings = {
        # "MONGO_COLLECTION": "middleschool_test",
        "MONGO_COLLECTION": "middleschool_test",
        "SPLASH_URL" : 'http://192.168.99.100:8050'
    }

    def start_requests(self):
        url='https://ip.cn'

        yield SplashRequest(
            url,
            endpoint='execute',
            args={
                'lua_source': lua_source,
            },
            callback=self.parseurl1
            )

    def parseurl1(self,response):
        ip=response.xpath('//*[@id="result"]/div/p/code/text()').extract_first()
        print(f"ip:{ip}")
