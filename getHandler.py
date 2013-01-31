from google.appengine.ext import db
from google.appengine.ext import webapp
from django.utils import simplejson

import datetime
import logging

import time
import base
import settings
import jsonrest
import models

class HostList(base.Base):
  def post(self):
    self.initSession()
    r = list()
    hosts = models.Host.all()
    for host in hosts:
      r.append(host.hostname)
    self.response.out.write(jsonrest.response(r))

    if settings.time_log:
      logging.info("Hostlist execution time %f" %(time.time() - self.t1))


class LastUpdate(base.Base):
  def post(self, hostname):
    self.initSession()
    host = models.getHostByName(hostname)
    q = models.Value.all()
    q = q.filter("host =", host).order("ctime")
    if q.count(limit=1) != 0:
      latest_values = q[0]
      ctime = jsonrest.strftime(latest_values.ctime)
      self.response.out.write(jsonrest.response(ctime))

    if settings.time_log:
      logging.info("LastUpdate execution time %f" %(time.time() - self.t1))


class ModuleList(base.Base):
  def post(self, hostname):
    self.initSession()
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
    if settings.time_log:
      logging.info("ModuleList execution time %f" %(time.time() - self.t1))
 
class MetricList(base.Base):
  def post(self, hostname, modulename):
    self.initSession()
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
    if settings.time_log:
      logging.info("MetricList execution time %f" %(time.time() - self.t1))


class Data(base.Base):
  def post(self, hostname, modulename, metricname):
    self.initSession()
    r = []
    host = models.getHostByName(hostname)
    if 'end_time' in self.post:
      end_time = datetime.datetime.strptime(self.post['end_time'], jsonrest.TIMEFORMAT)
    else:
      end_time = datetime.datetime.now()

    if 'start_time' in self.post:
      start_time = datetime.datetime.strptime(self.post['start_time'], jsonrest.TIMEFORMAT)
    else:
      start_time = end_time - settings.default_get_timerange

    if 'sampling' in self.post:
      sampling = int(self.post['sample'])
    else:
      sampling = settings.default_get_sampling

    if 'datatype' in self.post:
      if self.post['datatype'] == 'time_range':
        datatype = 'time_range'
      elif self.post['datatype'] == 'average':
        datatype = 'average'
      elif self.post['datatype'] == 'range':
        datatype = 'range'
      elif self.post['datatype'] == 'last':
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
    if settings.time_log:
      logging.info("GetData execution time %f" %(time.time() - self.t1))

class GetAllFromHostname(base.Base):
  def post(self, hostname):
    r = 0
    self.response.out.write(jsonrest.response(r))
