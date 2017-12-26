#!/usr/bin/env python
#-*- coding: utf-8 -*-
import BaseHandler
import settings
import hashlib
from tornado.web import authenticated

class MainHandler(BaseHandler.BaseHandler):
    @authenticated
    def get(self):
        self.render('index.html')

class DetailHandler(BaseHandler.BaseHandler):
    def get(self, url_hash):
        datas = self.db.get_detail(url_hash)
        if len(datas) == 0:
            self.write('None')
        else:
            self.render('detail.html', **datas)

class LoginHandler(BaseHandler.BaseHandler):
    def get(self):
        self.render('login.html')
    def post(self):
        username = self.get_argument('username', 'none')
        password = self.get_argument('password', 'none')
        check_hash = hashlib.md5(password+'__'+username).hexdigest()
        if check_hash != settings.CHECK_HASH:
            self.write('check error')
        else:
            self.set_secure_cookie("crawl_cookie", check_hash)
            self.redirect("/")
