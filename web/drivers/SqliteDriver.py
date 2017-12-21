#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sqlite3

class SqliteDriver():
    def __init__(self, settings):
        self.conn = sqlite3.connect(settings.DB_FILE)
        self.cursor = self.conn.cursor()
    def get_website(self):
        results = self.cursor.execute("select WEBSITE as website, count(*) as nums from crawl_data group by website").fetchall()
        return self.formatList(['website', 'num'], results)

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

