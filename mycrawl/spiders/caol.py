#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base
import re
import scrapy

class CaolScrapy(base.BaseScrapy):
    name = "caol"
    host = "http://t66y.com"
    start_url = "/thread0806.php?fid=7&search=&page=1"
    cat_id = '7'
    cat_name = '技术讨论区'
    url_keywords = 'htm_data'

    def get_item_urls(self, response):
        return response.xpath(u'//*[contains(@class, "tr3 t_one")]//h3//@href').extract()

    def get_next_page_url(self, response):
        next_page = response.xpath(u'//*[contains(text(), "下一頁")]/@href').extract()[0]
        if next_page:
            return self.host+self.start_url+next_page[0]
        return None

    def get_page_title(self, response):
        return response.xpath(u'//*[@class="tr1 do_not_catch"]//h4/text()').extract()[0]

    def get_page_content(self, response):
        return response.xpath(u'(//div[@class="tpc_content do_not_catch"])[1]').extract()[0]

    def get_page_pub_time(self, response):
        ptime = response.xpath(u'(//*[@class="tr1"])[1]//*[@class="tipad"]//text()').extract()
        ptime = ''.join(ptime)
        ptime = re.findall(r'(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2})', ptime)
        if ptime:
            ptime = ptime[0]
        return ''