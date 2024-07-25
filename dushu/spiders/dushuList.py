import scrapy
from scrapy import Request

from dushu.items import DushuItem, DushuItemLoader


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
            item_loader = DushuItemLoader(item=DushuItem(), response=response)
            item_loader.add_value('bookname', book.xpath('./div[@class="bookname"]/a/text()').extract_first())
            item_loader.add_value('author' , book.xpath('./div[@class="bookauthor"]/text()').extract_first())
            # FIX:图片下载需要 lsit 类型
            ingUrl = book.xpath('./div[@class="img152"]/a/img/@data-original').extract_first()
            item_loader.add_value("imgUrl", ingUrl)
            detailsUrl =  book.xpath('./div[@class="img152"]/a/@href').extract_first()
            item_loader.add_value('detailsUrl' ,detailsUrl)
            # 需要根据链接打开在提取

            yield scrapy.Request(url="https://www.dushu.com" + detailsUrl, meta={"item": item_loader},callback=self.details)



    def details(self,response):
        # TODO: 暂存对 loader 处理
        item_loader = response.meta.get("item", "")
        # 此处要用 Xath

        summary = response.xpath('//div[@class="book-summary"][1]//div[@class="text txtsummary"]/text()').extract_first()
        item_loader.add_value('summary', summary)


        item = item_loader.load_item()

        yield item











