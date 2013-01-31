from google.appengine.ext import db
from google.appengine.ext import webapp

import time
import urlparse
import jsonrest
import models
import datetime
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


class BenchDatastore(webapp.RequestHandler):
  def post(self, method='', count='1000'):
    count = int(count)
    host = models.getHostByName('peacewalker')
    starttime = datetime.datetime.now() - datetime.timedelta(minutes=count)
    endtime = datetime.datetime.now()
    values = '''
{"module1":{"metric1":1,"metric2":2,"metric3":3,"metric4":4},
,{"module2":{"metric1":1,"metric2":2,"metric3":3,"metric4":4},
,{"module3":{"metric1":1,"metric2":2,"metric3":3,"metric4":4},
,{"module4":{"metric1":1,"metric2":2,"metric3":3,"metric4":4}
'''
    t1 = time.time()
    if method == 'put':
      ctime = starttime
      for i in range(0,count):
        ctime += datetime.timedelta(minutes=1)
        v = models.Value(host=host, ctime=ctime, values=values)
        v.put()

    elif method == 'fetch':
      q = models.Value.all()
      q.filter("host =", host)
      q.filter("ctime >", starttime)
      q.filter("ctime <", endtime)
      for i in q:
        a = i.ctime
    
    logging.info('datastore bench %s time : %f' %(method, time.time()-t1))
    self.response.out.write(jsonrest.response('benchmark complete'))
