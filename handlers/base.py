#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import tornado.web

from tornado.escape import json_encode
from app.base import session
from settings import ROOT


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        if self.get_current_user() is None and not validator.is_whitelist(self.request.path):
            self.redirect('/login?next='+self.request.path+"&"+self.request.query)

    def get_current_user(self):
        user_name = self.get_secure_cookie("cookie_user_name")
        if not user_name:
            return None
        return session.execute("SELECT * FROM users WHERE name = %s", user_name)[0]

    def return_json(self, arg, status=200):
        self.set_status(status)
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.write(json_encode(arg))


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class RequestValidator:

    def __init__(self):

        self.whitelist_pattern = []
        self.whitelist = set()
        self.not_whitelist = set()

        with open(ROOT+'/conf/whitelist', 'r') as whitelist_file:
            for line in whitelist_file.readlines():
                line = line.strip()
                if line is not '' and not line.startswith('#'):
                        self.whitelist_pattern.append(line)

    def is_whitelist(self, path):
        if path in self.not_whitelist:
            return False
        if path in self.whitelist:
            return True
        for pattern in self.whitelist_pattern:
            if re.fullmatch(pattern, path):
                self.whitelist.add(path)
                return True
        self.not_whitelist.add(path)
        return False

validator = RequestValidator()