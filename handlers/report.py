from app.base import session
from handlers.base import BaseHandler

__author__ = 'wanggen'


class JobResultHandler(BaseHandler):
    # @tornado.web.authenticated
    def get(self, *args, **kwargs):
        job_id = self.get_argument('job_id', default='')
        job_results = session.execute("select * from spark_sql_job_results where job_id = %s", job_id)
        if self.request.headers['Accept'].__contains__('application/json'):
            self.return_json(job_results)
        else:
            self.render('/job/view', data=job_results, user=self.current_user)