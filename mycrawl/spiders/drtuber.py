#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base
import re
import scrapy
import json
from mycrawl.items import MycrawlItem

class DrtuberScrapy(base.BaseScrapy):
    name = "drtuber"
    host = "https://www.drtuber.com"
    start_url = "/asian"
    cat_id = 'asian'
    cat_name = 'asian'
    url_keywords = '.mp4'
    v_keywords = '/video/'
    vc_keywords = 'player_config_json'
    v_url = '/player_config_json?vid=%vid'

    def get_item_urls(self, response):
        urls = response.xpath(u'//a[@class="th ch-video"]//@href').extract()
        if urls:
            for i in range(len(urls)):
                urls[i] = self.host +'/'+ urls[i]
            return urls
        return []

    def get_next_page_url(self, response):
        next_page = response.xpath(u'//li[@class="next"]//a[contains(text(), "Next")]/@href').extract()
        if next_page:
            return self.host+'/'+next_page[0]
        return None

    def get_page_pub_time(self, response):
        ptime = response.xpath(u'(//*[@class="tr1"])[1]//*[@class="tipad"]//text()').extract()
        ptime = ''.join(ptime)
        ptime = re.findall(r'(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2})', ptime)
        if ptime:
            return ptime[0]
        return ''

    def parse(self, response):
        urls = self.get_item_urls(response)
        for url in urls[:]:
            yield scrapy.Request(url, callback=self.parse_post, errback=self.handle_error, dont_filter=True)
        next_page = self.get_next_page(response)
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse, errback=self.handle_error, dont_filter=True)

    def parse_post(self, response):
        if self.v_keywords in response.url:
            vid = re.findall(r' - (\d+) - ', response.xpath('//title//text()').extract_first())[0]
            v_config_url = self.host + self.v_url.replace('%vid', vid)
            yield scrapy.Request(v_config_url, callback=self.parse_post, errback=self.handle_error, dont_filter=True)
        elif self.vc_keywords in response.url:
            video_config = json.loads(response.body)
            video_url = None
            img_url = video_config['poster'] if video_config['poster'] else None
            if video_config['files']:
                video_url = video_config['files']['hq'] if video_config['files']['hq'] else video_config['files']['lq']
            self.is_ok = 1
            item = MycrawlItem()
            if not video_url or response.body == 'repeat':
                item['title'] = ''
                item['content'] = ''
                item['website'] = self.name
                item['url'] = video_url
                item['cat_id'] = self.cat_id
                item['cat_name'] = self.cat_name
                item['is_ok'] = self.is_ok
                item['pub_time'] = ''
            else:
                item['title'] = video_config['title']
                item['content'] = '<video class="crawl_video" src="'+video_url+'" poster="'+img_url+'" controls="controls"></video>'
                item['website'] = self.name
                item['url'] = video_url
                item['cat_id'] = self.cat_id
                item['cat_name'] = self.cat_name
                item['is_ok'] = self.is_ok
                item['pub_time'] = video_config['duration_format']
            yield item

