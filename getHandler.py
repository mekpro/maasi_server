from google.appengine.ext import db
from google.appengine.ext import webapp
from django.utils import simplejson

import logging
import jsonrest
import models

class HostList(webapp.RequestHandler):
  def post(self):
    r = list()
    hosts = models.Host.all()
    for host in hosts:
      r.append(host.hostname)
    self.response.out.write(jsonrest.response(r))

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
    metriclist = ['load1m','load5m','load15m','p_idle','p_active']
    self.response.out.write(jsonrest.response(metriclist))

class Data(webapp.RequestHandler):
  def post(self, hostname, modulename, metricname):
    r = [0,1,2,3,4,5,6,7]
    self.response.out.write(jsonrest.response(r))

class GetAllFromHostname(webapp.RequestHandler):
  def post(self, hostname):
    r = [1,2,3,4,5,6]
    self.response.out.write(jsonrest.response(r))
