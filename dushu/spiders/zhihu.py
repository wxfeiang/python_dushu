from typing import Iterable

import scrapy
from scrapy import Request

# from dushu.items import DushuItem, DushuItemLoader


class ZhiHuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ["https://www.zhihu.com"]
    custom_settings = {
        "COOKIES_ENABLED": True
    }
    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    # 模拟登录 拿到cookie
    def start_requests(self):

        pass




    def parse(self, response):
        pass











