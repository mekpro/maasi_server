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

def getValueModelFromTimeRange(start_time, end_time):
  # return models.Value
  tdelta = end_time - start_time
  if tdelta < (settings.aggregate_l1 * 10):
    logging.info('l0')
    return models.Value
  elif tdelta < (settings.aggregate_l2 * 10):
    logging.info('l1')
    return models.ValueL1
  else:
    logging.info('l2')
    return models.ValueL2

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

    logging.info("date range: %s - %s" %(start_time, end_time))
    q = getValueModelFromTimeRange(start_time, end_time)
    q = q.all()
    q.filter('host =', host)
    q.order('-ctime')
    logging.info("row count: %d" %q.count())

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

def parseQuery(query_json):
  d = {'peacewalker': {'loadavg' : ['load1m']}}
  return d

class GetAll(base.Base):
  def post(self, hostname):
    self.initSession()
    r = {}
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

    logging.info("date range: %s - %s" %(start_time, end_time))
    q = getValueModelFromTimeRange(start_time, end_time)
    q = q.all()
    q.filter('host =', host)
    q.order('-ctime')
    logging.info("row count: %d" %q.count())

    if datatype == 'last' or datatype == 'average':
      v = q[0]
      values = jsonrest.loads(v.values)
      r = values

    q.filter('ctime >', start_time).filter('ctime <', end_time)
    if datatype == 'range':
      counter = 0
      for v in q.run(limit=settings.query_rows_limit):
        values = jsonrest.loads(v.values)
        for module_name,metrics in values.items():
          if module_name not in r:
            r[module_name] = {}
          for metric_name,value in metrics.items():
            if metric_name not in r[module_name]:
              r[module_name][metric_name] = []
            else:
              r[module_name][metric_name].append((counter, values[module_name][metric_name]))
        counter += 1

    if datatype == 'time_range':
      for v in q.run(limit=settings.query_rows_limit):
        values = jsonrest.loads(v.values)
        for module_name,metrics in values.items():
          if module_name not in r:
            r[module_name] = {}
          for metric_name,value in metrics.items():
            if metric_name not in r[module_name]:
              r[module_name][metric_name] = []
            else:
              r[module_name][metric_name].append((str(v.ctime), values[module_name][metric_name]))

#    if datatype == 'average':

    self.response.out.write(jsonrest.response(r))
    if settings.time_log:
      logging.info("GetAllData execution time %f" %(time.time() - self.t1))



