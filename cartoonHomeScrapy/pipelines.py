# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from cartoonHomeScrapy.items import CartoonItem, CartoonMenu, CartoonDetail

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
        #判断item类型进入不同的sql
        if item.__class__ == CartoonItem:
            query_sql = """
                    select title from cartoon_base where title = %s
                    """
            query_params = item['title']
            update_sql = """
                        update cartoon_base set 
                        image_url = %s,
                        score = %s,
                        new_section = %s,
                        menu_url = %s
                        where title = %s
                    """
            update_params = (item['image_url'],
                         item['score'],
                         item['new_section'],
                         item['menu_url'],
                         item['title'])
            insert_sql = """
                        insert into cartoon_base(image_url, title, score, new_section ,menu_url)
                        value (%s, %s, %s, %s, %s)
                        """
            insert_params = (item['image_url'],
                             item['title'],
                             item['score'],
                             item['new_section'],
                             item['menu_url'])
        elif item.__class__ == CartoonMenu:
            query_sql = """
                        select title from cartoon_menu where title = %s
                        and num_section = %s
                    """
            query_params = (item['title'],item['num_section'])
            update_sql = """
                        update cartoon_menu set 
                        name_section = %s,
                        pic_num = %s,
                        detail_url = %s
                        where title = %s
                        and num_section = %s
                    """
            update_params = (item['name_section'],
                             item['pic_num'],
                             item['detail_url'],
                             item['title'],
                             item['num_section'])
            insert_sql = """insert into cartoon_menu(title, name_section, pic_num ,detail_url, num_section)
                        value (%s, %s, %s, %s,%s)"""
            insert_params = (item['title'],
                             item['name_section'],
                             item['pic_num'],
                             item['detail_url'],
                             item['num_section'])
        elif item.__class__ == CartoonDetail:
            query_sql = """
                select title from cartoon_detail where
                title = %s
                and num_section = %s
                and page_num = %s
            """
            query_params = (item['title'],
                            item['num_section'],
                            item['page_num'])
            update_sql = """
                update cartoon_detail set
                content_image_url = %s
                where title = %s
                and num_section = %s
                and page_num = %s
            """
            update_params = (item['content_image_url'],
                             item['title'],
                             item['num_section'],
                             item['page_num'])
            insert_sql = """
                insert into cartoon_detail(title,num_section,page_num,content_image_url)
                values(%s,%s,%s,%s)
            """
            insert_params = (item['title'],
                             item['num_section'],
                             item['page_num'],
                             item['content_image_url'])
        try:
            self.cursor.execute(query_sql, query_params)
            repeat = self.cursor.fetchone()
            # 如果存在进行更新
            if repeat:
                self.cursor.execute(update_sql, update_params)
                self.connect.commit()
            else:
                self.cursor.execute(insert_sql, insert_params)
                self.connect.commit()
        except Exception as e:
            print(e)
        return item

    def close_spider(self, spider):
        self.connect.close()


