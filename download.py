#!/usr/bin/env python3 
import conf
import urllib.request
import urllib.error
import os
import re

#read config
print("Reading config...")
cfg = conf.readConfig("config.cfg")

print("Downloading...")
for line in open("download.info"):
  line.strip()
  r = re.compile(r"((/[\w\_\d]+){3}/[\w\.\_\-\+\:\d]+\.tar\.xz)")
  match = r.search(line)
  if match:
    link = match.group(1)
    file_url = cfg.serv+link
    local_name = cfg.path+link
    if os.path.exists(os.path.dirname(local_name)) == False:
      os.makedirs(os.path.dirname(local_name))
    try:
      print("Loading: '{0}' to '{1}'".format(file_url,local_name))
      urllib.request.urlretrieve(file_url,local_name)
    except urllib.error.URLError as err:
      print(err)
      time.sleep(0.5)
    