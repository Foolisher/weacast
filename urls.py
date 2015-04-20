#!/usr/bin/env python
# -*- coding: utf-8 -*-
from handlers.base import IndexHandler

from handlers.job import *
from handlers.report import *
from handlers.user import *


url_patterns = [
    (r"/",             IndexHandler),
    (r"/login",        LoginHandler),
    (r"/logout",       LogoutHandler),
    (r"/jobs",         JobsListHandler),
    (r"/job",          JobHandler),
    (r"/job/result",   JobResultHandler)
]


