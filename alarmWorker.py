from google.appengine.ext import db
from google.appengine.ext import webapp

import time
import urlparse
import jsonrest
import models
import datetime
import logging
import settings

def put_host_down(host):
  logging.info("Host %s monitoring timeout, putting down" %host.hostname)
  host.state = down
  host.put()

def normal_interval_check():
  dt_timeout = datetime.datetime.now() - settings.host_timeout
  hosts = models.Host.all()
  hosts = hosts.filter("state =", "up")
  host_down = list() 
  for host in hosts:
    if host.last_update < dt_timeout:
      put_host_down(host)
      host_down.append(host.hostname)
  logging.info("Alarm normal interval check completed, %d host put down" %len(host_down))
  logging.info(host_down)

def custom_alarm_check():
  alarms = models.Alarm.all()

class AlarmWorker(webapp.RequestHandler):
  def post(self):
    normal_interval_check()
    custom_alarm_check()

