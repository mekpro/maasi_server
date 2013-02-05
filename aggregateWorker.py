from google.appengine.ext import db
from google.appengine.ext import webapp

import time
import urlparse
import jsonrest
import models
import datetime
import logging
import settings

def aggreate(values_list):
  return values_list[0]

class AggregateWorker(webapp.RequestHandler):
  def post():
    aggregate_dt_1 = datetime.datetime.now() - settings.aggregate_l1
    hosts = models.Hosts.all()
    hosts = hosts.filter("last_aggregate <", aggregate_dt_1)
    for host in hosts:
      starttime = host.last_aggregate
      endtime = starttime + setting.aggregate_l1
      values_list = models.values.all()
      values_list = values.filter("ctime >", starttime).filter("ctime <", endtime)
      values = aggregate(values_list)
      new_values = models.ValueL1(host=host, ctime=starttime, values=values)
      new_values.put()
      host.last_aggregate = endtime
      host.put()
      logging.info('aggregated %s' %host.hostname)

class CleanupWorker(webapp.RequestHandler):
  def post():
    values = models.Values.all()
    cleanup_dt = datetime.datetime.now() - settings.aggregate_cleanup
    values.filter("ctime <", cleanup_dt)
    values.fetch(10000)
    db.delete(values)
    logging.info('Clean up completed')
