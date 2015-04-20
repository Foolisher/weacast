# -*- coding: utf-8 -*-
import datetime
import sys
from tornado.options import options
from app.base import session

__author__ = 'wanggen'

import json
import logging
import httplib2
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def exec_sparkjob(job_id: str, sql: str, ttl: int):
    logging.info("rpc spark sql job:[%s]" % sql)
    conn = None
    try:
        conn = httplib2.HTTPConnectionWithTimeout(options.spark_server_host, port=options.spark_server_port, timeout=60 * 10)
        conn.request(method='POST', url='/sql', body=json.dumps({"job_id": job_id, "sql": sql, "async": "true", "ttl": ttl}))
        resp = conn.getresponse()
        logging.info("SparkJob[%s] invoke response:[%s]" % (job_id, resp.read().decode()))
    except Exception as e:
        logging.error("SparkSQL job execution error:%s " % sys.exc_info()[1])
        raise e
    finally:
        conn.close()


def stop_sparkjob(job_id: str):
    conn = None
    try:
        conn = httplib2.HTTPConnectionWithTimeout(options.spark_server_host, port=options.spark_server_port, timeout=60 * 10)
        conn.request(method='POST', url='/stop', body=json.dumps({"job_id": job_id}))
        resp = conn.getresponse()
        logging.info("SparkJob[%s] stop response:[%s]" % (job_id, resp.read().decode()))
    except Exception as e:
        logging.error("SparkSQL job stop error:%s " % sys.exc_info()[1])
        raise e
    finally:
        conn.close()


def create_sparkjob(job_id, sql, ttl, **cron_args):
    if scheduler.get_job(job_id) is not None:
        raise Exception('repeated job_id[%s]' % job_id)
    ttl = 60 * 60 * 24 * int(ttl)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    session.execute("INSERT INTO spark_sql_jobs (job_id, day, hour, sql, status, ttl, created_at)"
                    " VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    [job_id, cron_args['day'], cron_args['hour'], sql, '1', ttl, now])
    logging.info("Add job:%s" % job_id)
    scheduler.scheduled_job('cron', [job_id, sql, ttl], id=job_id, **cron_args)(exec_sparkjob)


def start_sparkjob(job_id):
    rows = session.execute("SELECT * FROM spark_sql_jobs where job_id='%s'" % job_id)
    if len(rows) > 0:
        exec_sparkjob(rows[0].job_id, rows[0].sql, rows[0].ttl)


def remove_sparkjob(job_id):
    scheduler.remove_job(job_id)
    session.execute("DELETE from spark_sql_jobs where job_id = '%s'" % job_id)


def exec_sparksql(sql):
    conn = None
    try:
        sql_str = sql
        logging.info('SQL:\n[%s]\nJSON_SQL:\n[%s]', sql_str, json.dumps({"sql": sql_str}))
        conn = httplib2.HTTPConnectionWithTimeout(options.spark_server_host, port=options.spark_server_port, timeout=60 * 5)
        conn.request(method='POST', url='/sql', body=json.dumps({"sql": sql_str, 'job_id': datetime.datetime.now().timestamp()*1000000}))
        resp = conn.getresponse()
        result = resp.read().decode(encoding='UTF-8', errors='strict')
        if resp.code == 500:
            return json.dumps({"error": result})
        else:
            return '{"data": %s}' % result
    except:
        logging.exception("SparkSQL job execution error")
        return json.dumps({'error': str(sys.exc_info()[1])})
    finally:
        conn.close()


executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 300
}

scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)


for job in session.execute('SELECT * FROM spark_sql_jobs'):
    logging.info("Add SparkSQL job[%s] hour[%s] sql[%s]" % (job['job_id'], job['hour'], job['sql'][0:50]))
    scheduler.scheduled_job('cron', [job['job_id'], job['sql'], job['ttl']], id=job['job_id'], day=job['day'], hour=job['hour'], second='0', minute='0')(exec_sparkjob)

scheduler.start()
