import scrapy
from scrapy import Request

from dushu.items import DushuItem

class DushulistSpider(scrapy.Spider):
    name = "dushuList"
    allowed_domains = ["www.dushu.com","img.dushu.com"]
    start_urls = ["https://www.dushu.com"]

    def parse(self, response):

        list = response.xpath('//div[@class="container margin-big-top padding-big-top"]')[1]
        # print(list)
        bookList = list.xpath('./div[1]//ul/li')
        #
        # print(bookList)
        for book in bookList:
            item= DushuItem()
            item['bookname'] = book.xpath('./div[@class="bookname"]/a/text()').extract_first()
            item['author'] = book.xpath('./div[@class="bookauthor"]/text()').extract_first()
            # FIX:图片下载需要 lsit 类型
            item['imgUrl'] = [book.xpath('./div[@class="img152"]/a/img/@data-original').extract_first()]
            item['detailsUrl'] = book.xpath('./div[@class="img152"]/a/@href').extract_first()
            # 需要根据链接打开在提取
            yield scrapy.Request(url="https://www.dushu.com"+item["detailsUrl"], callback=self.details ,meta={"item":item})



    def details(self,response):
        item = response.meta["item"]
        summary = response.xpath('//div[@class="book-summary"][1]//div[@class="text txtsummary"]/text()').extract_first()
        item['summary'] = summary
        yield item











