#!/usr/bin/env python
#-*- coding: utf-8 -*-
import BaseHandler

class MainHandler(BaseHandler.BaseHandler):
    def get(self):
        self.render('index.html')
