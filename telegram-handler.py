#!/usr/bin/env python3

import configparser
import os
import telebot
import change_configs as configs
import sys

tg_config_filename = 'tg.ini'
tg_section = 'TELEGRAM'

config_filename = 'settings.ini'
hosts_section = 'HOSTS'
led_section = 'LED'

config = configparser.ConfigParser()
config = configs.read_config(config_filename)

tg_config = configparser.ConfigParser()
tg_config = configs.read_config(tg_config_filename)

tg_admin_id = tg_config[tg_section]['admin_id']

tg_api_key = tg_config[tg_section]['api_key']
bot = telebot.TeleBot(tg_api_key)

@bot.message_handler(content_types=['text'])
def start(message):
  if str(message.from_user.id) != str(tg_admin_id):
    line = 'You are not allowed to use this bot. Your user_id below\n' + str(message.from_user.id)
    bot.send_message(message.from_user.id, line)
    return
  hosts_list = configs.show_hosts(config_filename, False)
#  config = configs.read_config(config_filename)

  print('GOT MSG: ' + message.text)
  if message.text == '/add_host':
    bot.send_message(message.from_user.id, hosts_list)
    bot.send_message(message.from_user.id, 'Enter pin number and hostname divided by whitespace')
    bot.register_next_step_handler(message, do_add_host)

  if message.text == '/del_host':
    bot.send_message(message.from_user.id, hosts_list)
    bot.send_message(message.from_user.id, 'Enter pin number (2-31)')
    bot.register_next_step_handler(message, do_del_host)

  if message.text == '/show_hosts':
    bot.send_message(message.from_user.id, hosts_list)

  if message.text == '/chng_bright':
    line = 'Current brihtness is: ' + str(config[led_section]['brightness']) + '\nInput new value (1-254)'
    bot.send_message(message.from_user.id, line)
    bot.register_next_step_handler(message, do_change_brightness)

  if message.text == '/chng_up_color':
    line = 'Current up color is: ' + str(config[led_section]['up_color']) + '\nInput new value (r,g,b)'
    bot.send_message(message.from_user.id, line)
    bot.register_next_step_handler(message, do_change_up_color)

  if message.text == '/chng_down_color':
    line = 'Current down color is: ' + str(config[led_section]['down_color']) + '\nInput new value (r,g,b)'
    bot.send_message(message.from_user.id, line)
    bot.register_next_step_handler(message, do_change_down_color)

  if message.text == '/show_conf':
    line = ''
    line = configs.show_config_full(config_filename, False)

    bot.send_message(message.from_user.id, 'Current config:')
    bot.send_message(message.from_user.id, line)


def do_del_host(message):
  led_pin = 33
  try:
    led_pin = int(message.text)
  except Exception:
    bot.send_message(message.from_user.id, 'It must be number (2-31)');
  led_pin = str(led_pin)
  line = 'Deleting host: ' + led_pin
  bot.send_message(message.from_user.id, line)
  print('del host: ' + led_pin)
  configs.del_key(config_filename, hosts_section, int(led_pin))


def do_add_host(message):
  msg_arr = str.split(message.text)
  led_pin = 0
  try:
    led_pin = int(msg_arr[0])
  except Exception:
    bot.send_message(message.from_user.id, 'Pin number must be a number (2-31)')
  led_pin = str(led_pin)
  host_itself = msg_arr[1]

  line = 'Adding host: ' + str(led_pin) + ' ' + str(host_itself)
  bot.send_message(message.from_user.id, line)
  print('add host: ' + str(led_pin) + ' ' + str(host_itself))
  configs.add_key(config_filename, hosts_section, led_pin, host_itself)

def do_change_brightness(message):
  new_brightness = int(message.text)
  configs.add_key(config_filename, led_section, 'brightness', new_brightness)
  line = 'Setting new brightness: ' + str(new_brightness)
  bot.send_message(message.from_user.id, line)

def do_change_up_color(message):
  new_color = str(message.text)
  configs.add_key(config_filename, led_section, 'up_color', new_color)
  line = 'Setting new up color: ' + str(new_color)
  bot.send_message(message.from_user.id, line)

def do_change_down_color(message):
  new_color = str(message.text)
  configs.add_key(config_filename, led_section, 'down_color', new_color)
  line = 'Setting new down color: ' + str(new_color)
  bot.send_message(message.from_user.id, line)

if __name__ == '__main__':

  if len(sys.argv) == 3:
    if os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
      config_filename = sys.argv[1]
      tg_config_filename = sys.argv[2]
    else:
      print("Invalid config filename, abort")
      exit()

  print(configs.show_hosts(config_filename, False))

  bot.infinity_polling()
