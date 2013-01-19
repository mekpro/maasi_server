from google.appengine.ext import db
from google.appengine.ext import webapp
import logging

import jsonrest
import models

class NewHost(webapp.RequestHandler):
  def post(self):
    post = jsonrest.parse_post(self.request.body)
    hostname = post['hostname']
    host = models.Host(hostname=hostname, configs='{}')
    host.put()
    logging.info('Host %s Created' %hostname)
    self.response.out.write(jsonrest.response(0))
