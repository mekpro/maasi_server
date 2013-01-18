import datetime
from google.appengine.ext import db

class Host(db.Model):
  name = db.StringProperty(required=True)
  last_update = db.DateTimeProperty(required=True, auto_now=True)
  state = db.StringProperty(required=True, choices=set(['up','down']), default="up")
  configs = db.StringProperty(required=True) # serialization of key,value

class Value(db.Model):
  instance = db.ReferenceProperty(Instance, required=True)
  ctime = db.DateTimeProperty(required=True, auto_now=True)
  values = db.StringProperty(required=True) # serialization of key,value
