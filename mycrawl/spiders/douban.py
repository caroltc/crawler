# -*- coding:utf-8 -*-
import scrapy
import re
from mycrawl.items import MycrawlItem

class DoubanScrapy(scrapy.Spider):
    name = "douban"
    host = "https://www.douban.com/group/explore"
    start_url = "https://www.douban.com/group/explore"

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//div[@class="channel-item"]//h3//@href').extract()
        for url in urls[:]:
            if 'topic' not in url:
                urls.remove(url)
                continue
            print url
            yield scrapy.Request(url, callback=self.parse_post, errback=self.handle_error, dont_filter=True)
        next_page = self.get_next_page(response)
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse, errback=self.handle_error, dont_filter=True)

    def get_next_page(self, response):
        next_page = response.xpath('//span[@class="next"]//a//@href').extract()[0]
        next_page_url = self.host+next_page
        max_page = self.settings.get('MAX_PAGE', 5*30)
        next_page_no = re.findall(r'start=(\d+)', next_page)
        if next_page_no:
            next_page_no = int(next_page_no[0])
        else:
            next_page_no = 30

        if next_page_no < max_page:
            return next_page_url
        else:
            return None


    def parse_post(self, response):
        item = MycrawlItem()
        item['title'] = response.xpath('//h1//text()').extract_first()
        item['content'] = response.xpath('//div[@id="link-report"]').extract_first()
        item['website'] = self.name
        item['url'] = response.url
        item['cat_id'] = 'explore'
        item['cat_name'] = u'话题精选'
        item['is_ok'] = 1
        item['pub_time'] = response.xpath('//h3//span[@class="color-green"]//text()').extract_first()
        yield item

    def handle_error(self, error):
        if 'topic' in url:
            yield scrapy.Request(url, callback=self.parse_post, errback=self.handle_error, dont_filter=True)
        else:
            yield scrapy.Request(next_page, callback=self.parse, errback=self.handle_error, dont_filter=True)


