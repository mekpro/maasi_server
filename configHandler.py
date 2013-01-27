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
