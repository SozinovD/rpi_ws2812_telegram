#!/usr/bin/env python3

import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import os
import time
import sys

from rpi_ws281x import PixelStrip, Color

import configparser

conf_filename = 'settings.ini'
hosts_section = 'HOSTS'
led_section = 'LED'

PING_WAIT = 2
SLEEP_SEC = 2

# LED strip configuration:
LED_COUNT = 32        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
#LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_BRIGHTNESS = 10
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

RED = Color(255,0,0)
GREEN = Color(0,255,0)


def_conf = configparser.ConfigParser()
def_conf[hosts_section] = {'0' : '8.8.8.8',
                           '1' : 'google.com'
                          }

def_conf[led_section] = { 'brightness' : '10',
                          'count' : '32'
                        }


def read_config_hosts(filename):
  config_r = configparser.ConfigParser()
  if os.path.isfile(filename) and not os.stat(filename).st_size == 0:
    config_r.read(filename)
  else:
    config_r[hosts_section] = def_conf[hosts_section]
  return config_r


def get_hosts_from_cfg(config_g):
  hosts_ = []
  for key in config_g[hosts_section]:
    host_ = [ key, config_g[hosts_section][key] ]
    hosts_.append(host_)
  return hosts_


def show_config(config_s):
  for key in config_s[hosts_section]:
    print(key, " = ", config_s[hosts_section][key])


def Display_Ping(hosts_):
  result = []
  for host in hosts_:
    ip = host[1]
    p = subprocess.Popen(
        ["ping", "-c", "1", "-W", str(PING_WAIT), ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    result.append(p)

  for host, p in zip(hosts_, result):
    returncode = p.wait()
    led_num = int(host[0])
    ip = str(host[1])
    if returncode == 0:
        strip.setPixelColor(led_num, GREEN)
        print("UP\t" + str(led_num) + "\t" + ip)
    else:
        strip.setPixelColor(led_num, RED)
        print("DOWN\t" + str(led_num) + "\t" + ip)
  strip.show()


if __name__ == '__main__':

  if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]) and not os.stat(sys.argv[1]).st_size == 0:
      conf_filename = sys.argv[1]
    else:
      print("Invalid config filename, abort")
      exit()

  config = configparser.ConfigParser()
  config = read_config_hosts(conf_filename)

  hosts = get_hosts_from_cfg(config)

  LED_BRIGHTNESS = int(config[led_section]['BRIGHTNESS'])
  LED_COUNT = int(config[led_section]['COUNT'])

  strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()

  while True:

    Display_Ping(hosts)
    print("___________")
    time.sleep(SLEEP_SEC)
