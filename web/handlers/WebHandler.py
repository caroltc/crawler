#!/usr/bin/env python
#-*- coding: utf-8 -*-
import BaseHandler

class MainHandler(BaseHandler.BaseHandler):
    def get(self):
        self.render('index.html')

class DetailHandler(BaseHandler.BaseHandler):
    def get(self, url_hash):
        datas = self.db.get_detail(url_hash)
        if len(datas) == 0:
            self.write('None')
        else:
            self.render('detail.html', **datas)
