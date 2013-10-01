#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado import websocket, web, ioloop, gen
import motor
import json

cl = []

class IndexHandler(web.RequestHandler):

    @web.asynchronous
    @gen.engine
    def get(self):
        """Display all messages
        """
        msgs = []
        db = self.settings['db']
        cursor = db.messages.find().sort([('_id', -1)])
        while (yield cursor.fetch_next):
            message = cursor.next_object()
            msgs.append(message['msg'])

        self.render("index.html", msgs=msgs)


class SocketHandler(websocket.WebSocketHandler):

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)

class ApiHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        self.finish()
        value = self.get_argument("value")
        data = {"value" : value}
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)


    @web.asynchronous
    @gen.engine
    def post(self):
        """Insert a message
        """
        self.finish()
        msg = self.get_argument("msg")

        db = self.settings['db']
        # motor.Op raises an exception on error, otherwise returns result
        result = yield motor.Op(db.messages.insert, {'msg': msg})

        jdata = {"msg" : msg}
        jdata = json.dumps(jdata)
        for c in cl:
            c.write_message(jdata)

