import datetime
from google.appengine.ext import db

class User(db.Model):
  username = db.StringProperty(required=True)
  password = db.StringProperty(required=True)
  session_key = db.StringProperty(default="")

class Host(db.Model):
  hostname = db.StringProperty(required=True)
  owner = db.ReferenceProperty(required=True)
  last_update = db.DateTimeProperty(required=True, auto_now=True)
  state = db.StringProperty(required=True, choices=set(['up','down']), default="up")
  configs = db.StringProperty(required=True) # serialization of key,value

class Value(db.Model):
  host = db.ReferenceProperty(Host, required=True)
  ctime = db.DateTimeProperty(required=True, auto_now=True)
  values = db.TextProperty(required=True) # serialization of key,value

class Alarm(db.Model):
  alarm_name = db.StringProperty(required=True)
  host = db.ReferenceProperty(Host, required=True)
  module = db.StringProperty(required=True)
  metric = db.StringProperty(required=True)
  value = db.FloatProperty(required=True)
  operand = db.StringProperty(required=True)

def getHostByName(hostname):
  hosts = Host.all()
  hosts = hosts.filter('hostname =', hostname)
  host = hosts[0]
  return host
