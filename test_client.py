from multiprocessing import Process
import sys

import time
import random
import jsonrest
import datetime

timezone = datetime.timedelta(hours=-7)

server_ip = "http://localhost:8080/"
#server_ip = "http://maasiserver.appspot.com/"
#server_ip = "http://10.1.1.186:8080/"

def clear_data(c):
  print c.request("admin/cleardatastore", {})
  print c.request("admin/newuser", {"username": "admin", "password": "password"})
  print c.request("authen/create_new_session_key", {"username": "admin", "password": "password"})

def generate_mockup_data():
  return  {
  "hostname": "peacewalker",
  "ctime": "2013-01-18 17:45:03",
  "values" : {
    "loadavg" : {
      "load1m" : 0.1,
      "load5m" : 0.2,
      "load15m" : 0.3,
      "p_active" : 1,
      "p_idle" : 100,
      },
    "netinterface" : {
      "eth0__rx" : 1,
      "eth0__tx" : 2,
      "eth1__rx" : 3,
      "eth1__tx" : 4,
      }
    }
  }

hosts = [
    'wata__fe',
    'wata__compute-0-0',
    'wata__compute-0-1',
    'wata__compute-0-2',
    'wata__compute-0-3',
    'wata__compute-0-4',
#    'wata__compute-0-5',
#    'wata__compute-0-6',
    'maeka__fe',
    'maeka__compute-0-0',
#    'maeka__compute-0-1',
#    'maeka__compute-0-2',
#    'maeka__compute-0-3',
    ]

def randomLogic():
  i = random.randint(0,1)
  if i == 1:
    return -1
  else:
    return 1

def simple_init(c, listen_count):
  listen_data = generate_mockup_data()
  print c.request("config/newhost", {"hostname": "peacewalker"})
  for i in range(0, listen_count):
    ctime = datetime.datetime.now() - datetime.timedelta(minutes=i) + timezone
    listen_data["ctime"] = jsonrest.strftime(ctime)
    print c.request("listen", listen_data)

def simple_test(c):
  listen_data = generate_mockup_data()
  print 'get: %s' %c.request("get", {})
  print 'get/peacewalker: %s' %c.request("get/peacewalker", {})
#  print 'get/peacewalker/last_update: %s' %c.request("get/peacewalker/last_update", {})
  print 'get/peacewalker/loadavg: %s' %c.request("get/peacewalker/loadavg", {})
  print 'get/peacewalker/loadavg/load1m: %s', c.request("get/peacewalker/loadavg/load1m", {'datatype':'range'})
  start_time = jsonrest.strftime(datetime.datetime.now() - datetime.timedelta(minutes=30) + timezone)
  end_time = jsonrest.strftime(datetime.datetime.now() + timezone)
  print 'get/peacewalker/loadavg/load1m(start-end): %s' %c.request("get/peacewalker/loadavg/load1m", {'start_time': start_time,'end_time': end_time, 'datatype':'range'})
  print 'get/peacewalker/loadavg/load1m(last): %s' %c.request("get/peacewalker/loadavg/load1m", {'datatype':'last'})
  print 'get/peacewalker/loadavg/load1m(average): %s' %c.request("get/peacewalker/loadavg/load1m", {'datatype':'average'})
  print 'get/peacewalker/loadavg/load1m(time_range): %s' %c.request("get/peacewalker/loadavg/load1m", {'datatype':'time_range'})
  print 'getall/peacewalker: %s' %c.request("getall/peacewalker", {'datatype':'range'})
  print 'config/alarm/add: %s' %c.request("config/alarm/add", {'alarm_name' :'alarm1', 'host_name': 'peacewalker', 'module_name': 'loadavg', 'metric_name':'load1m', 'operand':'lt', 'value': 2})
  print 'config/alarm/list: %s' %c.request("config/alarm/list", {})
  print 'config/alarm/remove: %s' %c.request("config/alarm/remove", {'alarm_name' :'alarm1'})
  print 'config/alarm: %s' %c.request("config/alarm", {})

def worker_test():
  print 'config/alarm/add: %s' %c.request("config/alarm/add", {'alarm_name' :'alarm1', 'host_name': 'peacewalker', 'module_name': 'loadavg', 'metric_name':'load1m', 'operand':'lt', 'value': 2})
  print 'config/alarm/list: %s' %c.request("config/alarm/list", {})
  print 'config/alarm/remove: %s' %c.request("config/alarm/remove", {'alarm_name' :'alarm1'})
  print 'config/alarm: %s' %c.request("config/alarm", {})
  print 'worker/alarm: %s' %c.request("worker/alarm", {})

class SimDataGenProcess(Process):
  def __init__(self, connection, host, listen_count):
    Process.__init__(self)
    self.c = connection
    self.host = host
    self.listen_count = listen_count

  def run(self):
    listen_data = generate_mockup_data()
    listen_data["hostname"] = self.host
    for i in range(0,self.listen_count):
      ctime = datetime.datetime.now() - datetime.timedelta(minutes=i) + timezone
      listen_data["ctime"] = jsonrest.strftime(ctime)
      listen_data["values"]["loadavg"]["load1m"] += 0.3 * randomLogic()
      listen_data["values"]["loadavg"]["load5m"] += 0.2 * randomLogic()
      listen_data["values"]["loadavg"]["load15m"] += 0.1 * randomLogic()
      listen_data["values"]["loadavg"]["p_active"] += 1 * randomLogic()
      listen_data["values"]["loadavg"]["p_idle"] += 1 * randomLogic()
      listen_data["values"]["netinterface"]["eth0__rx"] += 100 * randomLogic()
      listen_data["values"]["netinterface"]["eth0__tx"] += 10 * randomLogic()
      listen_data["values"]["netinterface"]["eth1__rx"] += 10 * randomLogic()
      listen_data["values"]["netinterface"]["eth1__tx"] += 10 * randomLogic()
      self.c.request("listen", listen_data)

def simulation_data_init(c, hosts, listen_count):
  process_list = []
  for host in hosts:
    print c.request("config/newhost", {"hostname": host})
  for host in hosts:
    p = SimDataGenProcess(c, host, 100)
    p.start()
    process_list.append(p)

  for p in process_list:
    while True:
      if p.is_alive():
        time.sleep(1)
      else:
        print "process %s completed" %str(p)
        break


def benchmark_method(c):
  listen_data = generate_mockup_data()
  simple_init(100)
  simulation_data_init(hosts, 1)
  print 'get: %s' %c.request("get", {})
  print 'get/peacewalker: %s' %c.request("get/peacewalker", {})
  print 'get/peacewalker/last_update: %s' %c.request("get/peacewalker/last_update", {})
  print 'get/peacewalker/loadavg: %s' %c.request("get/peacewalker/loadavg", {})
  print 'get/peacewalker/loadavg/load1m: %s', c.request("get/peacewalker/loadavg/load1m", {'datatype':'range'})
  print 'get/peacewalker/loadavg/load1m(last): %s' %c.request("get/peacewalker/loadavg/load1m", {'datatype':'last'})
  print c.request("listen", listen_data)

  # increase values size to test bigger listen package
  for i in range(0,10):
    listen_data["values"]["modules_"+str(i)] = dict()
    for j in range(0,10):
      listen_data["values"]["modules_"+str(i)]["metrics_"+str(j)] = j
  print c.request("listen", listen_data)

  #Another Increase
  for i in range(0,20):
    listen_data["values"]["modules_"+str(i)] = dict()
    for j in range(0,20):
      listen_data["values"]["modules_"+str(i)]["metrics_"+str(j)] = j
  print c.request("listen", listen_data)

def bench_datastore(c):
  simple_init(1)
  print c.request("admin/bench_datastore/put/100", {})
  print c.request("admin/bench_datastore/fetch/100", {})

def aggregate_test(c):
  for i in range(0,60):
    print 'aggregating %s' %c.request("worker/aggregate", {})
  start_time = jsonrest.strftime(datetime.datetime.now() - datetime.timedelta(minutes=120) + timezone)
  end_time = jsonrest.strftime(datetime.datetime.now() + timezone)
  print 'time: %s - %s ' %(str(start_time),str(end_time))
  print 'get/peacewalker/loadavg/load1m(start-end): %s' %c.request("get/wata__fe/loadavg/load1m", {'start_time': start_time,'end_time': end_time, 'datatype':'range'})

  start_time = jsonrest.strftime(datetime.datetime.now() - datetime.timedelta(minutes=600) + timezone)
  print 'get/peacewalker/loadavg/load1m(start-end): %s' %c.request("get/wata__fe/loadavg/load1m", {'start_time': start_time,'end_time': end_time, 'datatype':'range'})


if __name__ == '__main__':
  c = jsonrest.Client(server_ip)
  clear_data(c)
  key = c.request("authen/get_current_session_key", {"username": "admin", "password": "password"})
  print "session key: %s" , key
  c = jsonrest.Client(server_ip, key)

  simple_init(c,100)

  simple_test(c)
  # simulation_data_init(c,hosts, 100)
  # simulation_data_init(c,hosts, 10)
  # benchmark_method(c)
  # bench_datastore(c)
  # worker_test(c)
  # aggregate_test(c)
