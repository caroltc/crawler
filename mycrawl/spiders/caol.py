#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base
import re
import scrapy

class CaolScrapy(base.BaseScrapy):
    name = ""
    host = ""
    start_url = ""
    cat_id = '7'
    cat_name = ''
    url_keywords = ''

    def get_item_urls(self, response):
        urls = response.xpath(u'//*[contains(@class, "tr3 t_one")]//h3//@href').extract()
        if urls:
            for i in range(len(urls)):
                urls[i] = self.host +'/'+ urls[i]
            return urls
        return []

    def get_next_page_url(self, response):
        next_page = response.xpath(u'//*[contains(text(), "下一頁")]/@href').extract()
        if next_page:
            return self.host+'/'+next_page[0]
        return None

    def get_page_title(self, response):
        return response.xpath(u'//*[@class="tr1 do_not_catch"]//h4/text()').extract()[0]

    def get_page_content(self, response):
        if self.only_image == 1:
            imgs_a =  response.xpath(u'(//div[@class="tpc_content do_not_catch"])[1]//img//@src').extract()
            imgs_b = response.xpath(u'(//div[@class="tpc_content do_not_catch"])[1]//input[@type="image"]//@src').extract()
            return self.getImgContent(imgs_a+imgs_b)
        else:
            return response.xpath(u'(//div[@class="tpc_content do_not_catch"])[1]').extract_first()

    def get_page_pub_time(self, response):
        ptime = response.xpath(u'(//*[@class="tr1"])[1]//*[@class="tipad"]//text()').extract()
        ptime = ''.join(ptime)
        ptime = re.findall(r'(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2})', ptime)
        if ptime:
            return ptime[0]
        return ''
