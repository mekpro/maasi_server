from google.appengine.ext import db
from google.appengine.ext import webapp
from django.utils import simplejson
import datetime
import logging

import jsonrest
import models

def values_dumps(values_dict):
  return simplejson.dumps(values_dict)

class Listen(webapp.RequestHandler):
  def post(self):
    post = jsonrest.parse_post(self.request.body)
    hostname = post['hostname']
    ctime = post['ctime']
    values = post['values']

    ctime = datetime.datetime.strptime(ctime,"%Y-%m-%d %H:%M:%S")
    values_str = values_dumps(values)
    host = models.getHostByName(hostname)
    values = models.Value(host=host, ctime=ctime, values=values_str)
    values.put()

    self.response.out.write(jsonrest.response(0))
