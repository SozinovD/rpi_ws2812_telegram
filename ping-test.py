#!/usr/bin/env python3

import datetime
import subprocess

def ping_ip_addresses(ip_list):
  reachable = []
  unreachable = []
  result = []
  for ip in ip_list:
    print("start ping: " + ip)
    p = subprocess.Popen(
      ["ping", "-c", "1", "-W", '5', ip],
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
    )
    result.append(p)
  for ip, p in zip(ip_list, result):
    returncode = p.wait()
    if returncode == 0:
      reachable.append(ip)
    else:
      unreachable.append(ip)
  return reachable, unreachable

hosts = []
hosts.append("8.8.8.9")
hosts.append('8.8.8.8')
hosts.append('ya.ru')
hosts.append('10.125.133.1')
hosts.append('10.125.133.15')


print(datetime.datetime.now())
print(ping_ip_addresses(hosts))
print(datetime.datetime.now())

