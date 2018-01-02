#!/usr/bin/env python
#-*- coding: utf-8 -*-
import BaseHandler
import settings
import hashlib
import os
import json
from tornado.web import authenticated

class MainHandler(BaseHandler.BaseHandler):
    @authenticated
    def get(self):
        self.render('index.html')

class DetailHandler(BaseHandler.BaseHandler):
    @authenticated
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

class CollectionHandler(BaseHandler.BaseHandler):
    @authenticated
    def get(self, website, cat_id, data_id):
        result = self.db.addCollection(data_id, website, cat_id)
        if result:
            self.write('Success')
        else:
            self.write('Failed! Already Collected!')

class UploadHandler(BaseHandler.BaseHandler):
    @authenticated
    def get(self):
        self.write('''
<html>
  <head><title>Upload File</title></head>
  <body>
    <form action='upload' enctype="multipart/form-data" method='post'>
    <input type='file' name='file'/><br/>
    <input type='submit' value='submit'/>
    </form>
  </body>
</html>
            ''')
    def post(self):
        ret = {'result': 'OK'}
        upload_path = '../upload'  # 文件的暂存路径
        file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据
        if not file_metas:
            ret['result'] = 'Invalid Args'
            return ret

        for meta in file_metas:
            filename = meta['filename']
            file_path = os.path.join(upload_path, filename)

            with open(file_path, 'wb') as up:
                up.write(meta['body'])
                # OR do other thing

        self.write(json.dumps(ret))

class DownloadHandler(BaseHandler.BaseHandler):
    @authenticated
    def get(self):
        dir = '../upload'
        self.write('<ol>')
        for i in os.walk(dir):
            for k in i[2]:
                self.write('<li><a href="/download/do?file=%s">%s</a></li>'% (k, k))
        self.write('</ol>')

class DownloadDoHandler(BaseHandler.BaseHandler):
    @authenticated
    def get(self):
        filename = self.get_argument('file', 'none')
        dir = '../upload'
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename='+filename)
        with open(dir+'/'+filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        self.finish()