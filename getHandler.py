from google.appengine.ext import db
from google.appengine.ext import webapp

import jsonrest

class Hostlist():
  def post():
    hostlist = ['host1','host2','host3']
    self.response.out.write(jsonrest.response(hostlist))

class Modulelist():
  def post(hostname):
    modulelist = ['loadavg','netinterface']
    self.response.out.write(jsonrest.response(modulelist))

class MetricList():
  def post(hostname, modulename):
  metriclist = ['load1m','load5m','load15m','p_idle','p_active']
  self.response.out.write(jsonrest.response(metriclist))

class Data():
  def post(hostname, modulename, metricname):
    r = [0,1,2,3,4,5,6,7]
    self.response.out.write(jsonrest.response(r))
