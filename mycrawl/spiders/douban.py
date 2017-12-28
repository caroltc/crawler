#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base
import re
import scrapy

class DoubanScrapy(base.BaseScrapy):
    name = "douban"
    host = "https://www.douban.com"
    start_url = "/group/explore"
    cat_id = 'explore'
    cat_name = '话题精选'
    url_keywords = 'topic'

    def get_item_urls(self, response):
        return response.xpath('//div[@class="channel-item"]//h3//@href').extract()

    def get_next_page_url(self, response):
        next_page = response.xpath('//span[@class="next"]//a//@href').extract()
        if next_page:
            return self.host+self.start_url+next_page[0]
        return None

    def get_page_title(self, response):
        return response.xpath('//h1//text()').extract_first()

    def get_page_content(self, response):
        return response.xpath('//div[@id="link-report"]').extract_first()

    def get_page_pub_time(self, response):
        return response.xpath('//h3//span[@class="color-green"]//text()').extract_first()



