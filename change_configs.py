#!/usr/bin/env python3

import configparser
import os.path
import sys
import subprocess

config_filename = 'settings.ini'

hosts_section = 'HOSTS'
led_section = 'LED'

def_conf = configparser.ConfigParser()
def_conf[hosts_section] = {'0' : '8.8.8.8',
                           '1' : 'google.com'
                          }

def_conf[led_section] = { 'LED_BRIGHTNESS' : '10',
                          'LED_COUNT'   : '32',
                          'down_color'  : '255,0,0',
                          'up_color'    : '0,255,0'
                        }

def read_config(filename):
  config_r = configparser.ConfigParser()
  if os.path.isfile(filename) and not os.stat(filename).st_size == 0:
    config_r.read(filename)
  else:
    for section in def_conf.sections():
      config_r[section] = {}
      for key in def_conf[section]:
        config_r[section][key] = str(def_conf[section][key])
  return config_r

def write_to_file(config_w, config_filename_):
  with open(config_filename_, 'w') as configfile:
    config_w.write(configfile)
  restart_daemon()

def add_key(config_filename_, section, key, value):
  config_a = read_config(config_filename_)
  config_a[section][key] = str(value)
  write_to_file(config_a, config_filename_)
  return(config_a)

def del_key(config_filename_, section, key_to_del):
  new_config = configparser.ConfigParser()
  config_d = read_config(config_filename_)

  for section in config_d.sections():
    new_config[section] = {}
    for key in config_d[section]:
      if str(key) != str(key_to_del):
        new_config[section][key] = str(config_d[section][key])

  write_to_file(new_config, config_filename_)
  return(new_config)

def read_args():
  if len(sys.argv) > 3:
    print('\nInput 2 parameters to add host: led_pin and host(ip or DNS name), for example:')
    print(sys.argv[0] + ' 2 8.8.4.4')
    print('\nOr 1 parameter to delete host by led_pin, example:')
    print(sys.argv[0] + ' 2')
    print('\nOr no parameters to just show hosts')
    print('\nAbort')
    exit()
  if len(sys.argv) == 3:
    return(sys.argv[1], sys.argv[2])
  if len(sys.argv) == 2:
    return(sys.argv[1])

def restart_daemon():
  subprocess.run(['sudo', 'systemctl', 'restart', 'ledHat.service'])

def show_hosts(config_filename_, do_print):
  config_s = configparser.ConfigParser()
  config_s = read_config(config_filename_)
  line = ''
  for key in config_s[hosts_section]:
    line += key + " = " + config_s[hosts_section][key]
    line += '\n'
  if do_print != False:
    print(line)
  return line


if __name__ == '__main__':

  args_arr = read_args()

  if len(sys.argv) == 3:
    add_key(config_filename, hosts_section, args_arr[0], args_arr[1])

  if len(sys.argv) == 2:
    del_key(config_filename, hosts_section, args_arr[0])

  if len(sys.argv) == 1:
    show_hosts(config_filename, True)
