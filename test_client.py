import jsonrest
import datetime

c = jsonrest.Client("http://localhost:8080/")


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
for i in range(0,60):
  ctime = datetime.datetime.now() + datetime.timedelta(minutes=i)
  listen_data["ctime"] = datetime.datetime.strftime(ctime, jsonrest.TIMEFORMAT)
  print c.request("listen", listen_data)

print c.request("get", {})
print c.request("get/peacewalker", {})
print c.request("get/peacewalker/loadavg", {})
print c.request("get/peacewalker/loadavg/load1m", {'datatype':'range'})
start_time = jsonrest.strftime(datetime.datetime.now() - datetime.timedelta(minutes=30))
end_time = jsonrest.strftime(datetime.datetime.now())
print c.request("get/peacewalker/loadavg/load1m", {'start_time': start_time,'end_time': end_time, 'datatype':'range'})
print c.request("get/peacewalker/loadavg/load1m", {'datatype':'last'})

print c.request("getall/peacewalker", {})
