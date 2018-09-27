# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class CartoonItemPipeline(object):
    def __init__(self,settings):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into cartoon_base(image_url, title, score, new_section ,menu_url)
                value (%s, %s, %s, %s, %s)""",
                (item['image_url'],
                 item['title'],
                 item['score'],
                 item['new_section'],
                 item['menu_url']))
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
        return item

    def close_spider(self, spider):
        self.connect.close()
