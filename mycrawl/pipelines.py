# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import sqlite3
import time
import os

class MycrawlPipeline(object):
    def process_item(self, item, spider):
    	tdb = sqlite3.connect("mycrawl/data.db")
    	cursor = tdb.cursor()
    	save_data = self.check_item_exist(item, cursor)
    	if save_data:
            self.save_item(save_data, cursor)
        tdb.commit()
        cursor.close()
        tdb.close()
        return item

    def check_item_exist(self, item, cursor):
    	url_hash = hashlib.md5(item['url'].encode('utf-8')).hexdigest()
        results = cursor.execute("select ID from crawl_data where URL_HASH='%s'" % url_hash).fetchall()
        if len(results) > 0 :
        	return False
        item['url_hash'] = url_hash
        item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return item

    def save_item(self, item, cursor):
        result = cursor.execute("INSERT INTO crawl_data(URL_HASH,TITLE,URL,WEBSITE,CAT_ID,CAT_NAME,CONTENT,PUB_TIME,CRAWL_TIME,IS_OK) VALUES (?,?,?,?,?,?,?,?,?,?)",
            [item['url_hash'], item['title'], item['url'], item['website'], item['cat_id'], item['cat_name'], item['content'], item['pub_time'], item['crawl_time'], item['is_ok']])
        print result

