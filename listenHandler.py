from google.appengine.ext import db
from google.appengine.ext import webapp
from django.utils import simplejson
import datetime
import logging

import base
import jsonrest
import models
import time

import settings

class Listen(base.Base):
  def post(self):
    self.initSession()
    hostname = self.post['hostname']
    ctime = self.post['ctime']
    values = self.post['values']

    ctime = jsonrest.strptime(ctime)
    values_str = jsonrest.dumps(values)
#    logging.info(values_str)
    host = models.getHostByName(hostname)
    values = models.Value(host=host, ctime=ctime, values=values_str)
    values.put()

    self.response.out.write(jsonrest.response(0))
    if settings.time_log:
      logging.info("Listen Execution time %f", time.time() - self.t1)
