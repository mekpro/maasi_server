from google.appengine.ext import db
from google.appengine.ext import webapp
import logging

import base
import jsonrest
import models

class NewHost(base.Base):
  def post(self):
    self.initSession()
    hostname = self.post['hostname']
    host = models.Host(hostname=hostname, owner=self.user, configs='{}')
    host.put()
    logging.info('Host %s Created' %hostname)
    self.response.out.write(jsonrest.response(0))

class AlarmAdd(base.Base):
  def post(self):
    self.initSession()
    alarm_name = self.post['alarm_name']
    host_name = self.post['host_name']
    module_name = self.post['module_name']
    metric_name = self.post['metric_name']
    operand = self.post['operand']
    value = float(self.post['value'])

    host = models.getHostByName(host_name)
    alarm = models.Alarm(
      alarm_name=alarm_name,
      host=host,
      module=module_name,
      metric=metric_name,
      operand=operand,
      value=value,
    )
    alarm.put()
    self.response.out.write(jsonrest.response(0))

class AlarmRemove(base.Base):
  def post(self):
    self.initSession()
    alarm_name = self.post['alarm_name']
    alarms = models.Alarm.all()
    alarms.filter("alarm_name =", alarm_name)
    db.delete(alarms)
    self.response.out.write(jsonrest.response(0))

class AlarmList(base.Base):
  def post(self):
    r = []
    self.initSession()
    alarms = models.Alarm.all()
    for a in alarms:
      r.append(a.alarm_name)
    self.response.out.write(jsonrest.response(r))


