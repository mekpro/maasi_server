import sys

import jsonrest
import datetime
import random

def randomLogic():
  i = random.randint(0,1)
  if i == 1:
    return -1
  else:
    return 1

server_ip = "http://localhost:8080/"
listen_count = 60

c = jsonrest.Client(server_ip)

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

# Listen data format
listen_data = {
  "hostname": "peacewalker",
  "ctime": "2013-01-18 17:45:03",
  "values" : {
    "loadavg" : {
      "load1m" : 2.0,
      "load5m" : 0.5,
      "load15m" : 0.3,
      "p_active" : 5,
      "p_idle" : 100,
      },
    "netinterface" : {
      "eth0__rx" : 120,
      "eth0__tx" : 230,
      "eth1__rx" : 300,
      "eth1__tx" : 400,
      }
    }
  }

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
