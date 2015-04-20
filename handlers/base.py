#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from tornado.escape import json_decode, json_encode


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def prepare(self):

        pass

    def get_current_user(self):
        user_name = self.get_secure_cookie("cookie_user_name")
        if not user_name:
            return None
        return self.db.execute("SELECT * FROM users WHERE name = %s", str(user_name))[0]

    def return_json(self, arg, status=200):
        self.set_status(status)
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.write(json_encode(arg))


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")