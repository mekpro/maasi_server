import sys

import random
import jsonrest
import datetime

#server_ip = "http://localhost:8080/"
server_ip = "http://maasiserver.appspot.com/"

c = jsonrest.Client(server_ip)
print c.request("admin/newuser", {"username": "admin", "password": "password"})
print c.request("authen/create_new_session_key", {"username": "admin", "password": "password"})
key = c.request("authen/get_current_session_key", {"username": "admin", "password": "password"})
print "session key: %s" , key

# Re- Create Client with Session Key
c = jsonrest.Client(server_ip, key)

# Listen data format
listen_data = {
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
    'wata__compute-0-5',
    'wata__compute-0-6',
    'maeka__fe',
    'maeka__compute-0-0',
    'maeka__compute-0-1',
    'maeka__compute-0-2',
    'maeka__compute-0-3',
    ]

def randomLogic():
  i = random.randint(0,1)
  if i == 1:
    return -1
  else:
    return 1

def simple_init(listen_count):
  print c.request("config/newhost", {"hostname": "peacewalker"})
  for i in range(0, listen_count):
    ctime = datetime.datetime.now() - datetime.timedelta(minutes=i)
    listen_data["ctime"] = jsonrest.strftime(ctime)
    print c.request("listen", listen_data)

def simple_test():
  print 'get: %s' %c.request("get", {})
  print 'get/peacewalker: %s' %c.request("get/peacewalker", {})
  print 'get/peacewalker/last_update: %s' %c.request("get/peacewalker/last_update", {})
  print 'get/peacewalker/loadavg: %s' %c.request("get/peacewalker/loadavg", {})
  print 'get/peacewalker/loadavg/load1m: %s', c.request("get/peacewalker/loadavg/load1m", {'datatype':'range'})
  start_time = jsonrest.strftime(datetime.datetime.now() - datetime.timedelta(minutes=30))
  end_time = jsonrest.strftime(datetime.datetime.now())
  print 'get/peacewalker/loadavg/load1m(start-end): %s' %c.request("get/peacewalker/loadavg/load1m", {'start_time': start_time,'end_time': end_time, 'datatype':'range'})
  print 'get/peacewalker/loadavg/load1m(last): %s' %c.request("get/peacewalker/loadavg/load1m", {'datatype':'last'})
  print 'get/peacewalker/loadavg/load1m(average): %s' %c.request("get/peacewalker/loadavg/load1m", {'datatype':'average'})
  print 'get/peacewalker/loadavg/load1m(time_range): %s' %c.request("get/peacewalker/loadavg/load1m", {'datatype':'time_range'})

def simulation_data_init(hosts, listen_count):
  for host in hosts:
    print c.request("config/newhost", {"hostname": host})

  for host in hosts:
    for i in range(0,listen_count):
      ctime = datetime.datetime.now() - datetime.timedelta(minutes=i)
      listen_data["hostname"] = host
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
      c.request("listen", listen_data)

def benchmark_method():
  simple_init(1)
  #simulation_data_init(hosts, 1)
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

if __name__ == '__main__':
  #simple_init(1)
  #simple_test()
  benchmark_method()

