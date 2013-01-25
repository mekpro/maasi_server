from google.appengine.ext import db
from google.appengine.ext import webapp
from django.utils import simplejson

import datetime
import logging

import settings
import jsonrest
import models

class HostList(webapp.RequestHandler):
  def post(self):
    r = list()
    hosts = models.Host.all()
    for host in hosts:
      r.append(host.hostname)
    self.response.out.write(jsonrest.response(r))

class LastUpdate(webapp.RequestHandler):
  def post(self, hostname):
    host = models.getHostByName(hostname)
    q = models.Value.all()
    q = q.filter("host =", host).order("ctime")
    if q.count(limit=1) != 0:
      latest_values = q[0]
      ctime = jsonrest.strftime(latest_values.ctime)
      self.response.out.write(jsonrest.response(ctime))

class ModuleList(webapp.RequestHandler):
  def post(self, hostname):
    modules = []
    host = models.getHostByName(hostname)
    q = models.Value.all()
    q = q.filter("host =", host).order("ctime")
    if q.count(limit=1) != 0:
      latest_values = q[0]
      values = latest_values.values
      logging.info(values)
      vd = jsonrest.loads(values)
      for k,v in vd.iteritems():
        modules.append(k)
    self.response.out.write(jsonrest.response(modules))

class MetricList(webapp.RequestHandler):
  def post(self, hostname, modulename):
    metrics = []
    host = models.getHostByName(hostname)
    q = models.Value.all()
    q = q.filter("host =", host).order("ctime")
    if q.count(limit=1) != 0:
      latest_values = q[0]
      values = latest_values.values
      logging.info(values)
      vd = jsonrest.loads(values)
      vdm = vd[modulename]
      for k,v in vdm.iteritems():
        metrics.append(k)
    self.response.out.write(jsonrest.response(metrics))

class Data(webapp.RequestHandler):
  def post(self, hostname, modulename, metricname):
    r = []
    host = models.getHostByName(hostname)
    post = jsonrest.parse_post(self.request.body)
    if 'end_time' in post:
      end_time = datetime.datetime.strptime(post['end_time'], jsonrest.TIMEFORMAT)
    else:
      end_time = datetime.datetime.now()

    if 'start_time' in post:
      start_time = datetime.datetime.strptime(post['start_time'], jsonrest.TIMEFORMAT)
    else:
      start_time = end_time - settings.default_get_timerange

    if 'sampling' in post:
      sampling = int(post['sample'])
    else:
      sampling = settings.default_get_sampling

    if 'datatype' in post:
      if post['datatype'] == 'time_range':
        datatype = 'time_range'
      elif post['datatype'] == 'average':
        datatype = 'average'
      elif post['datatype'] == 'range':
        datatype = 'range'
      elif post['datatype'] == 'last':
        datatype = 'last'
    else:
      datatype = 'last'

    q = models.Value.all()
    q.filter('host =', host)
    q.order('-ctime')
    if datatype == 'last':
      v = q[0]
      values = jsonrest.loads(v.values)
      if modulename in values:
        if metricname in values[modulename]:
          r = (values[modulename][metricname])

    logging.info(start_time)
    logging.info(end_time)
    q.filter('ctime >', start_time).filter('ctime <', end_time)

    if datatype == 'range':
      counter = 0
      for v in q.run(limit=settings.query_rows_limit):
        values = jsonrest.loads(v.values)
        if modulename in values:
          if metricname in values[modulename]:
            r.append((counter, values[modulename][metricname]))
        counter += 1

    if datatype == 'time_range':
      for v in q.run(limit=settings.query_rows_limit):
        values = jsonrest.loads(v.values)
        if modulename in values:
          if metricname in values[modulename]:
            r.append((str(v.ctime), values[modulename][metricname]))

    if datatype == 'average':
      summation = 0.0
      count = 0
      for v in q.run(limit=settings.query_rows_limit):
        values = jsonrest.loads(v.values)
        if modulename in values:
          if metricname in values[modulename]:
            summation += (float(values[modulename][metricname]))
            count += 1
      r = summation / count

    self.response.out.write(jsonrest.response(r))

class GetAllFromHostname(webapp.RequestHandler):
  def post(self, hostname):
    r = 0
    self.response.out.write(jsonrest.response(r))
