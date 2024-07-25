import codecs
import json
import os

import pymysql
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline, DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



class DushuPipeline:
    def process_item(self, item, spider):
        return item

# 数据保存 JSON
class DushuJsonPipeline(object):

    # FIX: 固定写法
    def __init__(self):

        self.file = codecs.open("dushu.json", 'a', encoding='utf-8')
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(lines)

        return item

    def spider_closed(self, spider):
        self.file.close()

# json 数据导出
class JsonExportPipeline(object):

    def __init__(self):
        self.file = open("dushuExport.json" ,"wb")
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


# 加载 settings
from scrapy.utils.project import get_project_settings
# 保存到数据库
class DushuMysqlPipeline(object):
    def open_spider(self, spider):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.password = settings['DB_PASSWORD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']
        self.connect()

    def connect(self):
         self.conn = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,db=self.name,charset=self.charset)
         self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            sql = "insert into dushu(bookname,author,imgUrl,detailsUrl,summary) values(%s,%s,%s,%s,%s)"
            self.cursor.execute(sql,
                                (item['bookname'], item['author'], item['imgUrl'], item['detailsUrl'], item['summary']))
            self.conn.commit()
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
            self.conn.rollback()

        return item


    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()



# 图片下载

class DushuImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        headers = {
            'Referer': "https://img.dushu.com",
       }

        #
        # for image_url in item['imgUrl']:
        #     image_url = image_url
        #  图片以list形式
        yield scrapy.Request(item["imgUrl"],headers = headers)

    def item_completed(self, results, item, info):
        #FIX: 图片地址也可以替换为 本地资源图片地址
        if 'imgUrl' in item:
            for OK,value in results:
                if OK:
                    item["imgUrl"] = value["path"]
                else:
                    raise DropItem('Image Downloaded Failed')
        return item


