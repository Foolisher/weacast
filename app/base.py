from cassandra.cluster import Cluster
from cassandra.decoder import dict_factory
from tornado.options import options

__author__ = 'wanggen'


session = Cluster(contact_points=[options.cassandra_host]).connect(options.cassandra_keyspace)
session.row_factory = dict_factory