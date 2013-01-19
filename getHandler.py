from google.appengine.ext import db
from google.appengine.ext import webapp

import jsonrest
import models

class HostList(webapp.RequestHandler):
  def post(self):
    hostlist = ['host1','host2','host3']
    self.response.out.write(jsonrest.response(hostlist))

class ModuleList(webapp.RequestHandler):
  def post(self, hostname):
    modulelist = ['loadavg','netinterface']
    self.response.out.write(jsonrest.response(modulelist))

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
