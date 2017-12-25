#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sqlite3

class SqliteDriver():
    def __init__(self, settings):
        self.conn = sqlite3.connect(settings.DB_FILE)
        self.cursor = self.conn.cursor()

    def get_website(self):
        results = self.cursor.execute("select WEBSITE, count(*) from crawl_data group by website").fetchall()
        return self.formatList(['website', 'num'], results)

    def get_cat(self, website):
        results = self.cursor.execute("select CAT_ID, CAT_NAME, count(*) from crawl_data where WEBSITE = '%s' group by cat_id" % website).fetchall()
        return self.formatList(['cat_id', 'cat_name', 'num'], results)

    def get_list(self, website, cat_id, start, pagesize):
        count_results = self.cursor.execute("select count(*) from crawl_data where WEBSITE = '%s' and CAT_ID = '%s'" % (website,cat_id)).fetchall()
        results = self.cursor.execute("select WEBSITE, URL_HASH, CAT_ID, CAT_NAME, TITLE, PUB_TIME, CRAWL_TIME, IS_OK from crawl_data where WEBSITE = '%s' and CAT_ID = '%s' order by crawl_time desc limit %s,%s" % (website,cat_id,start,pagesize)).fetchall()
        list = self.formatList(['website', 'url_hash', 'cat_id', 'cat_name', 'title', 'pub_time', 'crawl_time', 'is_ok'], results)
        total = count_results[0][0]
        return {"list":list, "total":total}

    def get_search_list(self, website, keyword, start, pagesize):
        count_results = self.cursor.execute("select count(*) from crawl_data where WEBSITE = '%s' and TITLE like '%s'" % (website,'%'+keyword+'%')).fetchall()
        results = self.cursor.execute("select WEBSITE, URL_HASH, CAT_ID, CAT_NAME, TITLE, PUB_TIME, CRAWL_TIME, IS_OK from crawl_data where WEBSITE = '%s' and TITLE like '%s' order by crawl_time desc limit %s,%s" % (website,'%'+keyword+'%',start,pagesize)).fetchall()
        list = self.formatList(['website', 'url_hash', 'cat_id', 'cat_name', 'title', 'pub_time', 'crawl_time', 'is_ok'], results)
        total = count_results[0][0]
        return {"list":list, "total":total}

    def get_detail(self, url_hash):
        results = self.cursor.execute("select WEBSITE, URL_HASH, CAT_ID, CAT_NAME, TITLE, PUB_TIME, CRAWL_TIME, CONTENT, IS_OK  from crawl_data where  URL_HASH = '%s'" % url_hash).fetchall()
        datas = self.formatList(['website', 'url_hash', 'cat_id', 'cat_name', 'title', 'pub_time', 'crawl_time', 'content', 'is_ok'], results)
        if len(datas) > 0:
            return datas[0]
        return []

    def formatList(self, fields, results):
        if results:
            format_result = []
            for item in results:
                row_data = {}
                for index in range(len(fields)):
                    row_data[fields[index]] = item[index]
                format_result.append(row_data)
            return format_result
        else:
            return []

