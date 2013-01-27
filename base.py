from google.appengine.ext import db
from google.appengine.ext import webapp
from django.utils import simplejson

import logging

import settings
import jsonrest
import models

class Base(webapp.RequestHandler):
  def __init__(self, request=None, response=None):
    self.initialize(request, response)

  def initSession(self):
    self.post = jsonrest.parse_post(self.request.body)
    if 'session_key' in self.post:
      session_key = self.post['session_key']
      q = models.User.all().filter("session_key =", session_key)
      if q.count(limit=1) != 0:
        self.user = q[0]
      else:
        logging.info("Invalid session %s", session_key)
        exit(1)
    else:
      exit(1)
