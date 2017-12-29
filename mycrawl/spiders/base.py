#!/usr/bin/env python
#-*- coding:utf-8 -*-
import scrapy
import sys
from mycrawl.items import MycrawlItem

class BaseScrapy(scrapy.Spider):
    name = ""
    host = ""
    start_url = ""
    current_page = 1
    max_page = 1
    cat_id = ''
    cat_name = ''
    url_keywords = ''
    only_image = 0
    is_ok = 1

    def start_requests(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.getCommandParams();
        self.start_url = self.settings.get('START_URL', self.start_url)
        self.start_url = self.host+self.start_url
        self.max_page = self.settings.get('MAX_PAGE', self.max_page)
        self.max_page = int(self.max_page)
        self.cat_id = self.settings.get('CAT_ID', self.cat_id)
        self.cat_name = self.settings.get('CAT_NAME', self.cat_name)
        self.cat_name = unicode(self.cat_name)
        self.url_keywords = self.settings.get('URL_KEYWORDS', self.url_keywords)
        self.only_image = self.settings.get('ONLY_IMAGE', self.only_image)
        self.only_image = int(self.only_image)
        yield scrapy.Request(self.start_url, callback=self.parse)

    def parse(self, response):
        urls = self.get_item_urls(response)
        for url in urls[:]:
            if self.url_keywords not in url:
                urls.remove(url)
                continue
            yield scrapy.Request(url, callback=self.parse_post, errback=self.handle_error, dont_filter=True)
        next_page = self.get_next_page(response)
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse, errback=self.handle_error, dont_filter=True)

    def get_next_page(self, response):
        self.current_page = self.current_page + 1
        if self.max_page < self.current_page:
            return None
        return self.get_next_page_url(response)

    def parse_post(self, response):
        self.is_ok = 1
        item = MycrawlItem()
        if response.body == 'repeat':
            item['title'] = ''
            item['content'] = ''
            item['website'] = self.name
            item['url'] = response.url
            item['cat_id'] = self.cat_id
            item['cat_name'] = self.cat_name
            item['is_ok'] = self.is_ok
            item['pub_time'] = ''
        else:
            item['title'] = self.get_page_title(response)
            item['content'] = self.get_page_content(response)
            item['website'] = self.name
            item['url'] = response.url
            item['cat_id'] = self.cat_id
            item['cat_name'] = self.cat_name
            item['is_ok'] = self.is_ok
            item['pub_time'] = self.get_page_pub_time(response)

        yield item

    def handle_error(self, failure):
        print 'LOOK', failure.value
        # if self.url_keywords in response.url:
        #     yield scrapy.Request(response.url, callback=self.parse_post, errback=self.handle_error, dont_filter=True)
        # else:
        #     yield scrapy.Request(next_page, callback=self.parse, errback=self.handle_error, dont_filter=True)

    def getImgContent(self, imgs):
        if len(imgs) < 1:
            self.is_ok = 0
            return ''
        html_content = '<div class="client_show_images">'
        for i in range(len(imgs)):
            html_content =  html_content + '<p><img src="' +imgs[i]+ '"/></p>'
        return html_content+'</div>'

    def getCommandParams(self):
        return ''

    def get_item_urls(self, response):
        return []

    def get_next_page_url(self, response):
        return ''

    def get_next_page_no(self, next_page_url):
        return None

    def get_page_title(self, response):
        return ''

    def get_page_content(self, response):
        return ''

    def get_page_pub_time(self, response):
        return ''

    def get_page_url(self, response):
        return response.url