# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MycrawlItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    website = scrapy.Field()
    url = scrapy.Field()
    cat_id = scrapy.Field()
    cat_name = scrapy.Field()
    is_ok = scrapy.Field()
    pub_time = scrapy.Field()
    url_hash = scrapy.Field()
    crawl_time = scrapy.Field()
    pass
