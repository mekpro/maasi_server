import sys

import jsonrest
import datetime

server_ip = "http://localhost:8080/"
listen_count = 10

c = jsonrest.Client(server_ip)

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

print c.request("config/newhost", {"hostname": "peacewalker"})
for i in range(0,listen_count):
  ctime = datetime.datetime.now() - datetime.timedelta(minutes=i)
  listen_data["ctime"] = jsonrest.strftime(ctime)
  print c.request("listen", listen_data)

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

print c.request("getall/peacewalker", {})
