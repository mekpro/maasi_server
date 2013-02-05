from google.appengine.ext import db
from google.appengine.ext import webapp

import time
import urlparse
import jsonrest
import models
import datetime
import logging
import settings

def notify_host(msg, host):
  # TODO: send mail
  logging.info("Alarm: %s: %s" %(host.hostname, msg))

def timeout_interval_check():
  dt_timeout = datetime.datetime.now() - settings.host_timeout
  hosts = models.Host.all()
  hosts = hosts.filter("state =", "up")
  host_down = list()
  for host in hosts:
    if host.last_update < dt_timeout:
      put_host_down("interval timeout", host)
      host.state = down
      host.put()
      host_down.append(host.hostname)
  logging.info("Alarm normal interval check completed, %d host put down" %len(host_down))
  logging.info(host_down)

def custom_alarm_check():
  alarms = models.Alarm.all()
  for alarm in alarms:
    host = models.getHostByName(alarm.hostname)
    q = models.Value.all()
    q = q.filter("host =", host).order('ctime', 'desc')
    values = jsonrest.loads(q[0].values)
    if alarm.module_name in values:
      if alarm.metric_name in values[module_name]:
        v = values[module_name][metric_name]
        if alarm.operand == "gt" and alarm.value > v :
          notify_host("metric [%s][%s][%s] reached greater than" %(
            alarm.host_name, alarm.module_name, alarm.metric_name, alarm.value))

        elif alarm.openrand == "lt" and alarm.value < v :
          notify_host("metric [%s][%s][%s] reached lower than" %(
            alarm.host_name, alarm.module_name, alarm.metric_name, alarm.value))


class AlarmWorker(webapp.RequestHandler):
  def post(self):
    timeout_interval_check()
    custom_alarm_check()

