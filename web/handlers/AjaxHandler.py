#!/usr/bin/env python
#-*- coding: utf-8 -*-
import BaseHandler
import sys

class WebsiteHandler(BaseHandler.BaseHandler):
    def get(self):
        datas = self.db.get_website()
        return self.response_ok(datas)

class CatHandler(BaseHandler.BaseHandler):
    def get(self, website):
        datas = self.db.get_cat(website)
        return self.response_ok(datas)

class ListHandler(BaseHandler.BaseHandler):
    def get(self, website, cat_id, start, pagesize):
        reload(sys)
        sys.setdefaultencoding('utf8')
        keyword = self.get_argument('keyword', 'null')
        if keyword != 'null' or keyword != '':
            datas = self.db.get_search_list(website, unicode(keyword), start, pagesize)
        else:
            datas = self.db.get_list(website, cat_id, start, pagesize)
        return self.response_ok(datas)