# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class CartoonItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    image_url = Field()
    title = Field()
    score = Field()
    new_section = Field()
    menu_url = Field()

class CartoonMenu(Item):
    Id = Field()
    title = Field()
    name_section = Field()
    pic_num = Field()
    detail_url = Field()
    num_section = Field()

class CartoonDetail(Item):
    Id = Field()
    title = Field()
    num_section = Field()
    content_image_url = Field()
    page_num = Field()