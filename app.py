#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path

from tornado import websocket, web, ioloop, gen

from tornado.options import define, options

from urls import get_handlers_urls

import motor

define("port", default=8888, help="run on the given port", type=int)
db = motor.MotorClient('mongodb://localhost:27017').open_sync()['rpg_db']

class Application(web.Application):

    def __init__(self):
        handlers =  get_handlers_urls()
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            db = db
        )
        web.Application.__init__(self, handlers, **settings)


def main():
    print 'Listening on http://localhost:8888'
    options.parse_command_line()
    app = Application()
    app.listen(options.port)
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
