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
  dt_timeout = datetime.datetime.now() - datetime.timedelta(seconds=settings.host_timeout)
  hosts = models.Host.all()
  hosts = hosts.filter("state =", "up")
  for host in hosts:
    if host.ctime < dt_timeout:
      put_host_down(host)

def custom_alarm_check():
  alarms = models.Alarm.all()

class AlarmWorker(webapp.RequestHandler):
  def get(self):
    normal_interval_check()
    custom_alarm_check()

