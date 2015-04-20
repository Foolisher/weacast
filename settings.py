#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
import tornado.template
import os
from tornado.options import options, define


# Make filepaths relative to settings.
path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define('templates_home', default=ROOT+'/templates', help='web page templates root path')
define('port', default=8090, help='web server port')
define('debug', default=True, help='server debug mode')

define('spark_server_host', default='localhost', help='spark server host')
define('spark_server_port', default='9005', help='spark server port')


define('cassandra_host', default='localhost', help='cassandra host')
define('cassandra_keyspace', default=None, help='cassandra keyspace like database name')
define('cassandra_user', default=None, help='cassandra user name')
define('cassandra_password', default=None, help='cassandra user password')

tornado.options.parse_config_file(ROOT + '/conf/server.conf')
tornado.options.parse_command_line()


settings = {
    'debug': options.debug,
    'cookie_secret': "8226a97e61946beba18cec1eff50f743",
    'xsrf_cookies': False,
    'template_loader': tornado.template.Loader(options.templates_home),
    'login_url': '/login'
}

logging.config.fileConfig(ROOT + "/conf/logging.conf")

