import tornado
from tornado.web import authenticated
from app.base import session
from app.scheduler import remove_sparkjob, create_sparkjob, start_sparkjob, stop_sparkjob
from handlers.base import BaseHandler

__author__ = 'wanggen'


class JobsListHandler(BaseHandler):
    # @tornado.web.authenticated
    def get(self, *args, **kwargs):
        jobs = session.execute("select * from spark_sql_jobs")
        self.render('/jobs', jobs=jobs, user=self.current_user)


class JobHandler(BaseHandler):
    # @tornado.web.authenticated
    def get(self, *args, **kwargs):
        if self.request.headers['Accept'].__contains__('application/json'):
            job_id = self.get_argument('job_id', default='')
            if job_id is not '':
                job_id = " where job_id = '%s'" % job_id
            jobs = session.execute("select * from spark_sql_jobs %s " % job_id)
            self.return_json(jobs)
        else:
            jobs = session.execute("select * from spark_sql_jobs")
            self.render('/jobs', jobs=jobs, user=self.current_user)

    # @tornado.web.authenticated
    def post(self, *args, **kwargs):
        cron_args = {}
        job_id = self.get_argument('job_id')
        sql = self.get_argument('sql')
        ttl = self.get_argument('ttl', default=365)
        cron_args['day_of_week'] = self.get_argument('day_of_week', default='*')
        cron_args['day'] = self.get_argument('day', default='*')
        cron_args['hour'] = self.get_argument('hour')
        create_sparkjob(job_id=job_id, sql=sql, ttl=ttl, **cron_args)
        self.return_json({'resp': 'ok'})

    # @tornado.web.authenticated
    def delete(self, *args, **kwargs):
        job_id = self.get_argument('job_id')
        remove_sparkjob(job_id=job_id)
        self.return_json({'resp': 'ok'})


class JobStartHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        start_sparkjob(job_id=self.get_argument('job_id'))
        return self.return_json({'resp': 'ok'})


class JobStopHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        stop_sparkjob(job_id=self.get_argument('job_id'))
        return self.return_json({'resp': 'ok'})


