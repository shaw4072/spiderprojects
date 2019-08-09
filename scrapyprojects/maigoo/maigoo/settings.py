# -*- coding: utf-8 -*-

# Scrapy settings for maigoo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'maigoo'

SPIDER_MODULES = ['maigoo.spiders']
NEWSPIDER_MODULE = 'maigoo.spiders'

ROBOTSTXT_OBEY = False

################splash##################
SPLASH_URL = 'http://192.168.4.2:6213'
########################################
################proxypool###############
PROXY_DEFAULT="http://187.110.16.2:3128"
PROXYAPI="http://192.168.4.2:6220"
IPDBS="ipdbs"
########################################
#################mongodb################
MONGO_HOST = '192.168.4.2'
MONGO_PORT = 6017  # 端口号
MONGO_DB = "spider_maigoo"  # 库名
########################################
##################log###################
LOG_LEVEL= 'INFO'
# LOG_FILE ='log4.txt'
########################################
###############CONCURRENT###############
# CONCURRENT_REQUESTS = 32
# CONCURRENT_REQUESTS_PER_IP=0
# CONCURRENT_REQUESTS_PER_DOMAIN=32
########################################
############DOWNLOAD_DELAY##############
# DOWNLOAD_DELAY = 1+random()*1
DOWNLOAD_DELAY = 1
########################################
##############AUTOTHROTTLE##############
AUTOTHROTTLE_ENABLED=True
AUTOTHROTTLE_START_DELAY=3
########################################

ITEM_PIPELINES = {
   'maigoo.pipelines.StripPipeline':299,
   'maigoo.pipelines.MongoPipeline':301,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'maigoo.middlewares.GfUserAgentMiddleware': 539,  # 设置gf随机请求头
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 取消scrapy默认的请求头
    # 'maigoo.middlewares.SplashProxyPoolsMiddleware':724,     #设置ip2.0代理
    # 'maigoo.middlewares.SplashOneProxyPoolMiddleware': 721  # 设置固定ip代理
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

USER_AGENTS = [
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:55.0) Gecko/20100101 Firefox/55.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:55.0) Gecko/20100101 Firefox/55.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:55.0) Gecko/20100101 Firefox/55.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:55.0) Gecko/20100101 Firefox/55.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:55.0) Gecko/20100101 Firefox/55.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:55.0) Gecko/20100101 Firefox/54.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:55.0) Gecko/20100101 Firefox/53.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:55.0) Gecko/20100101 Firefox/52.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:55.0) Gecko/20100101 Firefox/50.0",
   "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2306.400 QQBrowser/9.5.10648.400",
   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
   "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
   "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
   "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
   "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]