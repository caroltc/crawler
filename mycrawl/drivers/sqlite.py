# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import sqlite3
import time
import os

class SqliteDriver():
    def __init__(self):
        self.tdb = sqlite3.connect("mycrawl/data.db")
        self.cursor = self.tdb.cursor()
        return None

    def get_item(self, item):
        if item['title'] == "" or (item['content'] == "" and item['is_ok'] == 1):
            return False
        url_hash = hashlib.md5(item['url'].encode('utf-8')).hexdigest()
        results = self.cursor.execute("select ID from crawl_data where URL_HASH='%s'" % url_hash).fetchall()
        url_hash = self.check_item_available(item['url'])
        if url_hash:
            item['url_hash'] = url_hash
            item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            return item
        return False

    def check_item_available(self, url):
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        results = self.cursor.execute("select ID from crawl_data where URL_HASH='%s'" % url_hash).fetchall()
        if len(results) > 0 :
            return False
        return url_hash

    def save_item(self, item):
        save_data = self.get_item(item)
        if save_data:
            result = self.cursor.execute("INSERT INTO crawl_data(URL_HASH,TITLE,URL,WEBSITE,CAT_ID,CAT_NAME,CONTENT,PUB_TIME,CRAWL_TIME,IS_OK) VALUES (?,?,?,?,?,?,?,?,?,?)",
            [item['url_hash'], item['title'], item['url'], item['website'], item['cat_id'], item['cat_name'], item['content'], item['pub_time'], item['crawl_time'], item['is_ok']])
            self.tdb.commit()
            return True
        return False

    def close(self):
        self.cursor.close()
        self.tdb.close()