from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import jsonrest
import getHandler
import configHandler
import listenHandler
import adminHandler
import authenHandler

class Homepage(webapp.RequestHandler):
  def get(self):
    self.response.out.write('hello maasi server')

def main():
  application = webapp.WSGIApplication([
    (r'/', Homepage),
    (r'/authen/get_current_session_key', authenHandler.GetCurrentSessionKey),
    (r'/authen/create_new_session_key', authenHandler.CreateNewSessionKey),
    # get Handlers
    (r'/get/(.*)/(.*)/(.*)', getHandler.Data),
    (r'/get/(.*)/last_update', getHandler.LastUpdate),
    (r'/get/(.*)/(.*)', getHandler.MetricList),
    (r'/get/(.*)', getHandler.ModuleList),
    (r'/get', getHandler.HostList),
    (r'/getall/(.*)', getHandler.GetAllFromHostname),

    # listen Handlers
    (r'/listen', listenHandler.Listen),

    # config Handlers
    (r'/config/newhost', configHandler.NewHost),

    # admin Handlers 
    (r'/admin/newuser', adminHandler.NewUser),
    (r'/admin/cleardatastore', adminHandler.ClearDatastore),

    ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()

