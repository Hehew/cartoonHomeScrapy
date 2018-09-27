# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
from cartoonHomeScrapy.items import CartoonItem
import json



class CartoonhomeSpider(scrapy.Spider):
    name = 'cartoonHome'
    allowed_domains = ['www.dm5.com/manhua-list']
    start_urls = ['http://www.dm5.com/manhua-list/']
    base_url = 'http://www.dm5.com'

    def start_requests(self):
        yield Request(
            url='http://www.dm5.com/manhua-list/',
            callback=self.parse_all_cartoon
        )

    def parse(self, response):
        pass

    def parse_all_cartoon(self, response):
        results = response.css('.mh-item')
        for result in results:
            item = CartoonItem()
            item['image_url'] = re.match('background-image.*?\((.*?)\)', result.css('.mh-cover::attr(style)').extract_first()).group(1)
            item['title'] = result.css('.mh-item-detali .title a::text').extract_first()
            item['score'] = re.match('.*?star-(\d+).*?',result.css('.mh-item-detali .zl .mh-star-line::attr(class)').extract_first()).group(1)
            item['new_section'] = result.css('.mh-item-detali .chapter a::text').extract_first()
            item['menu_url'] = self.base_url + result.css('.mh-item-detali .title a::attr(href)').extract_first()
            yield item