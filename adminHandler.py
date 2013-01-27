from google.appengine.ext import db
from google.appengine.ext import webapp

import jsonrest
import models

class NewUser(webapp.RequestHandler):
  def post(self):
    post = jsonrest.parse_post(self.request.body)
    #check duplicate name
    q = models.User.all().filter("username =", post["username"])
    if q.count(limit=1) != 0:
      self.response.out.write("Duplicated username: %s" %post["username"])
      exit(1)
    else:
      user = models.User(username=post["username"], password=post["password"])
      user.put()
      self.response.out.write("User created: %s" %user.username)

