#!/usr/bin/env python3

import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import os
import time
import sys

from rpi_ws281x import PixelStrip, Color

import configparser

import change_configs as configs

config_filename = 'settings.ini'
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

DOWN_COLOR = Color(222,125,41)
UP_COLOR = Color(193,97,229)

def_conf = configparser.ConfigParser()
def_conf[hosts_section] = {'0' : '8.8.8.8',
                           '1' : 'google.com'
                          }

def_conf[led_section] = { 'brightness' : '10',
                          'count' : '32',
                          'down_color' : '255,0,0',
                          'up_color' : '0,255,0'
                        }


def get_hosts_from_cfg(config_g):
  hosts_ = []
  for key in config_g[hosts_section]:
    host_ = [ key, config_g[hosts_section][key] ]
    hosts_.append(host_)
  return hosts_


def Display_Ping(hosts_, up_color_, down_color_):
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
        strip.setPixelColor(led_num, up_color_)
        print("UP\t" + str(led_num) + "\t" + ip)
    else:
        strip.setPixelColor(led_num, down_color_)
        print("DOWN\t" + str(led_num) + "\t" + ip)
  strip.show()


if __name__ == '__main__':

  if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]) and not os.stat(sys.argv[1]).st_size == 0:
      config_filename = sys.argv[1]
    else:
      print("Invalid config filename, abort")
      exit()

  config = configparser.ConfigParser()
  config = configs.read_config(config_filename)

  hosts = get_hosts_from_cfg(config)
  print(hosts)

  up_color_arr = str(config[led_section]['up_color']).split(",")
  UP_COLOR = Color(int(up_color_arr[0]), int(up_color_arr[1]), int(up_color_arr[2]))

  down_color_arr = str(config[led_section]['down_color']).split(",")
  DOWN_COLOR = Color(int(down_color_arr[0]), int(down_color_arr[1]), int(down_color_arr[2]))

  LED_BRIGHTNESS = int(config[led_section]['BRIGHTNESS'])
  LED_COUNT = int(config[led_section]['COUNT'])

  strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()

  while True:

    Display_Ping(hosts, UP_COLOR, DOWN_COLOR)
    print("___________")
    time.sleep(SLEEP_SEC)
