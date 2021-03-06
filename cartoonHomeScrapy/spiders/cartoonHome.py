# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request
from cartoonHomeScrapy.items import CartoonItem, CartoonMenu, CartoonDetail


class CartoonhomeSpider(scrapy.Spider):
    name = 'cartoonHome'
    allowed_domains = ['www.dm5.com']
    start_urls = ['http://www.dm5.com/manhua-list']
    base_url = 'http://www.dm5.com'
    page = 0
    detail_url = ''

    def start_requests(self):
        yield Request(
            url='http://www.dm5.com/manhua-list/',
            callback=self.parse_all_cartoon
        )
        # yield Request(
        #     url='http://www.dm5.com/manhua-haizeiwang-onepiece/',
        #     callback=self.parse_menu
        # )
        # yield Request(url='http://www.dm5.com/m696448',callback=self.list_all_detail)

    def parse_cartoon_detail(self, response):
        item = CartoonDetail()
        item['title'] = response.css('div.title > span:nth-child(2) > a::text').extract_first()
        item['num_section'] = re.match('.*?(\d+).*?',response.css('div.title > span.active.right-arrow::text').extract_first()).group(1)
        item['content_image_url'] = response.css('#cp_image::attr(src)').extract_first()
        item['page_num'] = response.css('#chapterpager > span.current::text').extract_first()
        yield item

    #列出所有本集漫画中的request url
    def list_all_detail(self, response):
        begin_url = response.url[:-1]
        end_page = response.css('#chapterpager > a:last-child::text').extract_first()
        if end_page:
            end_page_num = int(end_page)
        # item = CartoonDetail()
        # item['title'] = response.css('div.title > span:nth-child(2) > a::text').extract_first()
        # item['num_section'] = re.match('.*?(\d+).*?',response.css('div.title > span.active.right-arrow::text').extract_first()).group(1)
        # item['content_image_url'] = response.css('#cp_image::attr(src)').extract_first()
        # item['page_num'] = response.css('#chapterpager > span.current::text').extract_first()
        for page in range(1, end_page_num + 1):
            if page == 1:
                print(begin_url)
                yield Request(url=begin_url, callback=self.parse_cartoon_detail)
            else:
                print(begin_url + '-p' + str(page) + '/')
                yield Request(url=begin_url + '-p' + str(page) + '/',callback=self.parse_cartoon_detail)

    # 解析漫画目录
    def parse_menu(self, response):
        title = response.css('.info > p.title::text').extract_first()
        menus = response.css('#detail-list-select-1 > ul > li')
        for menu in menus:
            item = CartoonMenu()
            item['title'] = title.strip()
            item['name_section'] = menu.css('a::text').extract_first().strip()
            if item['name_section']:
                item['num_section'] = re.match('.*?(\d+).*?',item['name_section']).group(1)
            if menu.css('a > span::text').extract_first():
                item['pic_num'] = menu.css('a > span::text').extract_first().strip()[1:-1]
            item['detail_url'] = self.base_url + menu.css('a::attr(href)').extract_first()
            yield item
            yield Request(url=item['detail_url'],callback=self.list_all_detail)

    def parse_all_cartoon(self, response):
        results = response.css('.mh-item')
        #没有数据不在爬取
        if results:
            for result in results:
                item = CartoonItem()
                item['image_url'] = re.match('background-image.*?\((.*?)\)', result.css('.mh-cover::attr(style)').extract_first()).group(1)
                item['title'] = result.css('.mh-item-detali .title a::text').extract_first()
                item['score'] = re.match('.*?star-(\d+).*?',result.css('.mh-item-detali .zl .mh-star-line::attr(class)').extract_first()).group(1)
                item['new_section'] = result.css('.mh-item-detali .chapter a::text').extract_first()
                item['menu_url'] = self.base_url + result.css('.mh-item-detali .title a::attr(href)').extract_first()
                self.page += 1
                yield item
                #爬取漫画具体目录
                yield Request(url=item['menu_url'],callback=self.parse_menu)
                #爬取下一页
                yield Request(url=self.start_urls[0] + '-p' + str(self.page) + '/',callback=self.parse_all_cartoon)

