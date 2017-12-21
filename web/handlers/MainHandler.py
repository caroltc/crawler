#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        website = self.db.get_website()
        self.render('index.html')
