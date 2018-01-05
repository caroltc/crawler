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

    def get_list(self, website, cat_id, start, pagesize, get_content = False):
        content_field = "'' as CONTENT" if not get_content else "CONTENT"
        count_results = self.cursor.execute("select count(*) from crawl_data where WEBSITE = '%s' and CAT_ID = '%s'" % (website,cat_id)).fetchall()
        results = self.cursor.execute("select WEBSITE, URL_HASH, CAT_ID, CAT_NAME, TITLE, PUB_TIME, CRAWL_TIME, IS_OK, %s from crawl_data where WEBSITE = '%s' and CAT_ID = '%s' order by crawl_time desc limit %s,%s" % (content_field, website,cat_id,start,pagesize)).fetchall()
        list = self.formatList(['website', 'url_hash', 'cat_id', 'cat_name', 'title', 'pub_time', 'crawl_time', 'is_ok', 'content'], results)
        total = count_results[0][0]
        return {"list":list, "total":total}

    def get_search_list(self, website, keyword, start, pagesize, get_content = False):
        content_field = "'' as CONTENT" if not get_content else "CONTENT"
        count_results = self.cursor.execute("select count(*) from crawl_data where WEBSITE = '%s' and TITLE like '%s'" % (website,'%'+keyword+'%')).fetchall()
        results = self.cursor.execute("select WEBSITE, URL_HASH, CAT_ID, CAT_NAME, TITLE, PUB_TIME, CRAWL_TIME, IS_OK, %s from crawl_data where WEBSITE = '%s' and TITLE like '%s' order by crawl_time desc limit %s,%s" % (content_field, website,'%'+keyword+'%',start,pagesize)).fetchall()
        list = self.formatList(['website', 'url_hash', 'cat_id', 'cat_name', 'title', 'pub_time', 'crawl_time', 'is_ok', 'content'], results)
        total = count_results[0][0]
        return {"list":list, "total":total}

    def get_detail(self, url_hash):
        results = self.cursor.execute("select ID, WEBSITE, URL, URL_HASH, CAT_ID, CAT_NAME, TITLE, PUB_TIME, CRAWL_TIME, CONTENT, IS_OK  from crawl_data where  URL_HASH = '%s'" % url_hash).fetchall()
        datas = self.formatList(['id', 'website', 'url', 'url_hash', 'cat_id', 'cat_name', 'title', 'pub_time', 'crawl_time', 'content', 'is_ok'], results)
        if len(datas) > 0:
            return datas[0]
        return []

    def addCollection(self, data_id, website, cat_id):
        count_results = self.cursor.execute("select count(*) from collection where DATA_ID = '%s'" % str(data_id)).fetchall()
        print count_results
        if int(count_results[0][0]) > 0:
            return False
        self.cursor.execute("INSERT INTO collection(DATA_ID, WEBSITE, CAT_ID) VALUES('%s', '%s', '%s')" % (str(data_id), website, cat_id))
        self.conn.commit()

        return True

    def get_collection_list(self, website, start, pagesize, get_content = False):
        content_field = "'' as CONTENT" if not get_content else "CONTENT"
        count_results = self.cursor.execute("select count(*) from collection where WEBSITE = '%s'" % website).fetchall()
        ids_result = self.cursor.execute("select ID from collection where WEBSITE = '%s' order by ID desc limit %s,%s" % (website,start,pagesize)).fetchall()
        ids_list = []
        list = []
        if ids_result:
            for i in range(len(ids_result)):
                ids_list.append(str(ids_result[i][0]))
            results = self.cursor.execute("select WEBSITE, URL_HASH, CAT_ID, CAT_NAME, TITLE, PUB_TIME, CRAWL_TIME, IS_OK, %s from crawl_data where ID IN ('%s')" % (content_field, ','.join(ids_list))).fetchall()
            list = self.formatList(['website', 'url_hash', 'cat_id', 'cat_name', 'title', 'pub_time', 'crawl_time', 'is_ok', 'content'], results)
        total = count_results[0][0]
        return {"list":list, "total":total}

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

