import urllib2
import urllib
import urlparse
import logging
import datetime

try:
  import simplejson
except ImportError:
  from django.utils import simplejson

TIMEFORMAT="%Y-%m-%d %H:%M:%S"

def strftime(dt):
  return datetime.datetime.strftime(dt, TIMEFORMAT)

def strptime(st):
  return datetime.datetime.strptime(st, TIMEFORMAT)

class Client():
  def __init__(self, server_url, session_key=None):
    self.server_url = server_url
    self.session_key = session_key

  def request(self, method, param={}):
    result_str = ""
    try:
      if self.session_key is not None:
        param["session_key"] = self.session_key
      params = urllib.urlencode(param)
      url = self.server_url + method
      f = urllib2.urlopen(url, params)
      result_str = f.read()
    except urllib2.URLError, e:
      logging.error("URL error:%s %s" % (url,str(e)))

    try:
      result = simplejson.loads(result_str)
      return result
    except:
      logging.error("error loading json'%s'" %result_str)

def response(datadict):
  try:
    result_str = simplejson.dumps(datadict)
    return result_str
  except:
    logging.error("error dumping json'%s'" %result_str)

def parse_post(params):
  try:
    r = urlparse.parse_qsl(params)
    return dict(r)
  except:
    logging.error("error decoding post'%s'" %params)

def dumps(datadict):
  r = simplejson.dumps(datadict)
  r = r.replace('\"','')
  r = r.replace('\'','\"')
  #logging.info(r)
  return r

def loads(datastr):
  return simplejson.loads(datastr)
