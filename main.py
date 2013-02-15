from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import jsonrest
import getHandler
import configHandler
import listenHandler
import adminHandler
import authenHandler
import alarmWorker
import aggregateWorker

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
    (r'/getall/(.*)', getHandler.GetAll),

    # listen Handlers
    (r'/listen', listenHandler.Listen),

    # config Handlers
    (r'/config/newhost', configHandler.NewHost),
    (r'/config/alarm/add', configHandler.AlarmAdd),
    (r'/config/alarm/remove', configHandler.AlarmRemove),
    (r'/config/alarm/list', configHandler.AlarmList),
    (r'/config/alarm', configHandler.AlarmList),

    # worker handlers
    (r'/worker/alarm', alarmWorker.AlarmWorker),
    (r'/worker/aggregate', aggregateWorker.AggregateWorker),
    (r'/worker/cleanup', aggregateWorker.CleanupWorker),

    # admin Handlers 
    (r'/admin/noop', adminHandler.NoOp),
    (r'/admin/newuser', adminHandler.NewUser),
    (r'/admin/cleardatastore', adminHandler.ClearDatastore),
    (r'/admin/bench_datastore/(.*)/(.*)', adminHandler.BenchDatastore),

    ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()

