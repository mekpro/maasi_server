from google.appengine.ext import db
from google.appengine.ext import webapp

import datetime
import logging
import random
import base64

import settings
import jsonrest
import models

def gen_key(length):
  nbits = length * 6 + 1
  bits = random.getrandbits(nbits)
  uc = u"%0x" % bits
  newlen = int(len(uc) / 2) * 2 # we have to make the string an even length
  ba = bytearray.fromhex(uc[:newlen])
  return base64.urlsafe_b64encode(str(ba))[:length]

class CreateNewSessionKey(webapp.RequestHandler):
  def post(self):
    post = jsonrest.parse_post(self.request.body)
    q = models.User.all()
    q.filter("username =", post["username"])
    q.filter("password =", post["password"])
    if q.count(limit=1) != 1:
      self.response.out.write("Invalid username or password")
      exit(0)
    else:
      user = q[0]
      session_key = gen_key(settings.session_key_length)
      user.session_key = session_key
      user.put()
      self.response.out.write(jsonrest.response(user.session_key))

class GetCurrentSessionKey(webapp.RequestHandler):
  def post(self):
    post = jsonrest.parse_post(self.request.body)
    q = models.User.all()
    q.filter("username =", post["username"])
    q.filter("password =", post["password"])
    if q.count(limit=1) != 1:
      self.response.out.write("Invalid username or password")
      exit(0)
    else:
      user = q[0]
      self.response.out.write(jsonrest.response(user.session_key))
