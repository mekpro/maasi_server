from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import jsonrest
import getHandler
import configHandler
import listenHandler
import adminHandler

def main():
  application = webapp.WSGIApplication([
    (r'/', Homepage),
    # get Handlers
    (r'/get', getHandler.Hostlist),
    (r'/get/(.*)', getHandler.Modulelist),
    (r'/get/(.*)/(.*)', getHandler.Metriclist),
    (r'/get/(.*)/(.*)/(.*)', getHandler.Data),
    (r'/getall/(.*)', getHandler.GetAllFromHostname),

    # listen Handlers
    (r'/listen', listenHandler.Listen),

    # config Handlers
    (r'/config/newhost', configHandler.NewHost),

    # admin Handlers 
    (r'/admin/cleardata', adminHandler.ClearDataHandler),

    ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()

