from google.appengine.ext import db
from google.appengine.ext import webapp

import time
import urlparse
import jsonrest
import models
import datetime
import logging
import settings

def aggregate(values_list):
  values = values_list[0].values
  logging.info(values)
  return values

class AggregateWorker(webapp.RequestHandler):
  def post(self):
    aggregate_dt_1 = datetime.datetime.now() - settings.aggregate_l1
    hosts = models.Host.all()
    hosts = hosts.filter("last_aggregate <", aggregate_dt_1)
    for host in hosts:
      start_time = host.last_aggregate
      end_time = start_time + settings.aggregate_l1
      logging.info(start_time)
      q = models.Value.all()
      q = q.filter("host =", host)
      q = q.filter("ctime >", start_time).filter("ctime <", end_time)
      if q.count(limit=1) > 0:
        values = aggregate(q)
        new_values = models.ValueL1(host=host, ctime=start_time, values=values)
        new_values.put()
        logging.info('aggregated %s' %host.hostname)
      else:
        logging.info('skipped %s on date %s' %(host.hostname, str(start_time)))
      host.last_aggregate = end_time
      host.put()
    self.response.out.write(jsonrest.response(0))

class CleanupWorker(webapp.RequestHandler):
  def post(self):
    values = models.Value.all()
    cleanup_dt = datetime.datetime.now() - settings.aggregate_cleanup
    values.filter("ctime <", cleanup_dt)
    values.fetch(10000)
    db.delete(values)
    logging.info('Clean up completed')
    self.response.out.write(jsonrest.response(0))
