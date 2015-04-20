#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.base import session
from handlers.base import BaseHandler
import logging


class LoginHandler(BaseHandler):
    def get(self):
        self.render("user/login.html", next=self.get_argument("next", "/"))

    def post(self):
        name = self.get_argument("name")
        user = session.execute("SELECT * FROM users WHERE name = %s", name)[0]
        if not user:
            logging.error("user(name=%s) not exist", name)
            self.return_json({"cause": 'user.not.exist'}, 400)
            # self.redirect("/user_not_exist")
            return

        if user['status'] != 1:
            logging.error("user(name=%s) status is not normal")
            self.return_json({"cause": "user.status.abnormal"}, 500)
            return

        if user['password'] != self.get_argument("password"):
            logging.error("user(name=%s) password mismatch", name)
            self.return_json({"cause": "password.mismatch"}, 500)
            return

        self.set_secure_cookie("cookie_user_name", str(user['name']), expires_days=None)
        self.redirect(self.get_argument("next", "/"))


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("cookie_user_name")
        self.redirect(self.get_argument("next", "/"))


