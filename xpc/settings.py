# -*- coding: utf-8 -*-

# Scrapy settings for xpc project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xpc'

SPIDER_MODULES = ['xpc.spiders']
NEWSPIDER_MODULE = 'xpc.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

HTTPPROXY_ENABLED = True

PROXIES = [
   'http://47.100.185.114:1703',
   'http://211.159.154.164:1703',
   'http://47.100.173.4:1703',
   'http://47.97.253.250:1703',
   'http://203.195.162.28:1703',
   'http://140.143.143.19:1703',
   'http://106.15.188.107:1703',
   'http://47.100.168.105:1703',
   'http://47.100.176.209:1703',
   'http://47.100.42.205:1703',
   'http://47.100.126.62:1703',
   'http://47.100.169.34:1703',
   'http://101.132.193.81:1703',

]
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4
# 超时时长
DOWNLOAD_TIMEOUT = 10

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'xpc.middlewares.XpcSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'xpc.middlewares.RandomProxyMiddleware': 702,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'xpc.pipelines.MysqlPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# redis配置
SCHEDUIER = 'scrapy_redis.scheduler.Scheduler'
# 确保所有的爬虫通过redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 将清除的项目在redis进行处理
ITEM_PIPELINES = {
   'xpc.pipelines.MysqlPipeline': 300,
   # 增加redis中间件
   # 'scrapy_redis.pipelines.RedisPipeline': 301,
}
# redis 地址
REDIS_URL = 'redis://127.0.0.1:6379'
SCHEDULER_PERSIST = True

#
COOKIES_ENABLED = True
COOKIES_DEBUG = True
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
   'Accept-Encoding': 'gzip, deflate',
   'Accept-Language': 'zh-CN,zh;q=0.9',
   'Cache-Control': 'max-age=0',
   'Connection': 'keep-alive',
   'Cookie': 'Device_ID=5b0b717682f81; Authorization=2852BAFDE2FEB5DE5E2FEB43E0E2FEB9747E2FEB11B033742A8B; _ga=GA1.2.1865357791.1527476603; zg_did=%7B%22did%22%3A%20%22163a4b392ef205-0e93cc7d9ef7f2-3b7c015b-f3000-163a4b392f1234%22%7D; UM_distinctid=163a4b39d8c7a-074b12300a7709-3b7c015b-f3000-163a4b39d8e15f; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22163a4b3fbad15-02563ab85b8cf2-3b7c015b-995328-163a4b3fbb04b%22%2C%22%24device_id%22%3A%22163a4b3fbad15-02563ab85b8cf2-3b7c015b-995328-163a4b3fbb04b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; bdshare_firstime=1527561484831; PHPSESSID=k142oo0rq9i0flanbobbpvp1e4; _gid=GA1.2.1582268173.1527731737; CNZZDATA1262268826=1840425648-1527472121-http%253A%252F%252Fwww.xinpianchang.com%252F%7C1527729099; Hm_lvt_dfbb354a7c147964edec94b42797c7ac=1527476654,1527560143,1527731738; zg_c9c6d79f996741ee958c338e28f881d0=%7B%22sid%22%3A%201527731737.268%2C%22updated%22%3A%201527733282.513%2C%22info%22%3A%201527476622099%2C%22cuid%22%3A%2010345127%7D; ts_uptime=0; Hm_lpvt_dfbb354a7c147964edec94b42797c7ac=1527733283; responseTimeline=608; cn_1262268826_dplus=%7B%22distinct_id%22%3A%20%22163a4b39d8c7a-074b12300a7709-3b7c015b-f3000-163a4b39d8e15f%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201527734631%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201527734631%7D%7D',
   'Host': 'www.xinpianchang.com',
   'Upgrade-Insecure-Requests': '1',
   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}
