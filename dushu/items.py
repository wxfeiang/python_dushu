# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


# 还可以对里面的每一个值 处理

def add_space(value):
    return value + '----当前------》 '

class DushuItem(scrapy.Item):
    bookname = scrapy.Field()
    author = scrapy.Field()
    imgUrl = scrapy.Field()
    detailsUrl = scrapy.Field()
    summary = scrapy.Field()
    pass
