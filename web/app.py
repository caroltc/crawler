import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import settings
import sqlite3
from handlers import *
from drivers import *

def make_app():
    db = None
    if settings.DB_TYPE == 'sqlite':
        db = SqliteDriver(settings)
    handlers = [
    (r"/", MainHandler, dict(db=db)),
    (r"/ajaxGetWebsite", WebsiteHandler, dict(db=db)),
    (r"/ajaxGetCat/(\w+)", CatHandler, dict(db=db)),
    (r"/login", MainHandler),
    ]
    config = {"template_path":settings.TEMPLATE_PATH, "static_path":settings.ASSETS_PATH, "debug":True}
    return tornado.web.Application(handlers, **config)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(settings.SERVER_PORT)
    tornado.ioloop.IOLoop.instance().start()