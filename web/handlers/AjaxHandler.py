#!/usr/bin/env python
#-*- coding: utf-8 -*-
import BaseHandler

class WebsiteHandler(BaseHandler.BaseHandler):
    def get(self):
        datas = self.db.get_website()
        return self.response_ok(datas)

class CatHandler(BaseHandler.BaseHandler):
    def get(self, website):
        datas = self.db.get_cat(website)
        return self.response_ok(datas)
