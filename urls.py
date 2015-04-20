#!/usr/bin/env python
# -*- coding: utf-8 -*-
from handlers.base import IndexHandler

from handlers.job import *
from handlers.report import *

from handlers.user import *
from handlers.application import *
from handlers.deployment import *
from handlers.host import *


url_patterns = [
    (r"/", IndexHandler),
    (r"/login",             LoginHandler),
    (r"/logout",            LogoutHandler),
    (r"/apps",              AppListHandler),
    (r"/apps/json",         AppListJsonHandler),
    (r"/apps/create",       AppCreateHandler),
    (r"/app/(\d)+",         AppViewHandler),
    (r"/app/(\d)+/edit",    AppUpdateHandler),
    (r"/deploy-prototype/create", DeployPrototypeCreateHandler),
    (r"/app/(\d)+/hosts",   HostListHandler),
    (r"/app/(\d)+/hosts/create", HostCreateHandler),
    (r"/job/result",        JobResultHandler),
    (r"/job", JobHandler),
    (r"/jobs", JobsListHandler)
]
