from google.appengine.ext import db
from google.appengine.ext import webapp

import urlparse
import jsonrest
import models
import logging

class NewUser(webapp.RequestHandler):
  def post(self):
    post = jsonrest.parse_post(self.request.body)
    logging.info(post)
    username = post["username"]
    password = post["password"]
    #check duplicate name
    q = models.User.all().filter("username =", username)
    if q.count(limit=1) != 0:
      self.response.out.write("Duplicated username: %s" %username)
      exit(1)
    else:
      user = models.User(username=username, password=password)
      user.put()
      self.response.out.write(jsonrest.response("User created: %s" %user.username))

class ClearDatastore(webapp.RequestHandler):
  def post(self):
    for q in (models.User, models.Host, models.Value):
      entries = q.all()
      entries.fetch(10000)
      db.delete(entries)
    self.response.out.write(jsonrest.response('datastore cleared'))
