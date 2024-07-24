
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


# 还可以对里面的每一个值 处理

def add_jobbole(value):
    return value + '自定义后缀------'


class DushuItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()

class DushuItem(scrapy.Item):
    bookname = scrapy.Field()
    author = scrapy.Field(
        input_processor = MapCompose(add_jobbole)
    )
    imgUrl = scrapy.Field()
    detailsUrl = scrapy.Field()
    summary = scrapy.Field()
    pass
