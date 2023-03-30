#!/usr/bin/env python3

import os
from os import listdir
from os.path import isfile, join

def format_bytes(size):
  # 2**10 = 1024
  power = 2**10
  n = 0
  power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
  while size > power:
    size /= power
    n += 1
  return round(size, 1), power_labels[n]+'B'


def list(dir):
  info_arr = []
  with os.scandir(dir) as dir_entries:
    for entry in dir_entries:
      info = entry.stat()
      info_formatted = '`' + entry.name + '` ' + str(format_bytes(info.st_size))
      info_arr.append(info_formatted)
  files_list = '\n'.join(info_arr)
  return files_list

def rm(dir, name):
  full_path = os.path.join(dir, name)
  if not os.path.isfile(full_path):
    return 'File not found'
  try:
    os.remove(full_path)
    line = 'File removed successfully:\n' + full_path
    return line
  except Exception as e:
    return e


#print(list('files'))
