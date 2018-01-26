#!/usr/bin/env python
#-*- coding: utf-8 -*-
import BaseHandler
import sys
import json
from tornado.web import authenticated

class WebsiteHandler(BaseHandler.BaseHandler):
    @authenticated
    def get(self):
        datas = self.db.get_website()
        return self.response_ok(datas)

class CatHandler(BaseHandler.BaseHandler):
    @authenticated
    def get(self, website):
        datas = self.db.get_cat(website)
        return self.response_ok(datas)

class ListHandler(BaseHandler.BaseHandler):
    @authenticated
    def get(self, website, cat_id, start, pagesize):
        reload(sys)
        sys.setdefaultencoding('utf8')
        keyword = self.get_argument('keyword', 'null')
        get_content = self.get_argument('get_content', 'N')
        show_content = True if get_content == 'Y' else False
        if keyword != 'null' and keyword != '':
            datas = self.db.get_search_list(website, unicode(keyword), start, pagesize, show_content)
        elif cat_id == 'none':
            datas = self.db.get_collection_list(website, start, pagesize, show_content)
        else:
            datas = self.db.get_list(website, cat_id, start, pagesize, show_content)
        return self.response_ok(datas)

class DeleteDataHandler(BaseHandler.BaseHandler):
    @authenticated
    def post(self):
        param = self.request.body.decode('utf-8')
        prarm = json.loads(param)
        self.db.delete_data(prarm['ids'])
        return self.response_ok()