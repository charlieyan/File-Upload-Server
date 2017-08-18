# -*- coding: utf-8 -*-

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app

PORT = 80
LOGGING = False

try:
    if LOGGING:
        from tornado.log import enable_pretty_logging
        enable_pretty_logging()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(PORT)
    print("Server started at port {}...\n".format(PORT))
    IOLoop.instance().start()
except Exception as ex:
    print("ERROR:", ex)