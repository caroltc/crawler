# -*- coding: utf-8 -*-
import scrapy
from mycrawl.items import MycrawlItem

class QuotesScrapy(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = []
    base_url = 'http://quotes.toscrape.com/page/%page/'
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  #设置浏览器用户代理

    def __init__(self, start_page=1, end_page=1, *args, **kwargs):
        super(QuotesScrapy, self).__init__(*args, **kwargs)
        urls = []
        for i in range(int(start_page), int(end_page)+1):
            urls.append(self.base_url.replace('%page', str(i)));
        self.start_urls = urls

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            item = MycrawlItem()
            item['title'] = quote.xpath('span[@class="text"]/text()').extract_first()
            item['content'] = quote.extract()
            item['website'] = self.name
            item['url'] = quote.xpath('span[@class="text"]/text()').extract_first()
            item['cat_id'] = 0
            item['cat_name'] = 'Default'
            item['is_ok'] = 1
            item['pub_time'] = ''
            yield item