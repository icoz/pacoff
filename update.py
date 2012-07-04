#!/usr/bin/env python3 
import conf
import urllib.request
import urllib.error
import os
import time

#read config
print("Reading config...")
cfg = conf.readConfig("config.cfg")
links=[]
for repo in cfg.repos:
  for arch in cfg.archs:
    link = "{serv}/{repo}/os/{arch}/{repo}".format(serv=cfg.serv,repo=repo,arch=arch)
    local = "{path}/{repo}/os/{arch}/{repo}".format(path=cfg.path,repo=repo,arch=arch)
    links.append((local+".db",link+".db"))
    links.append((local+".files",link+".files"))
#downloading
print("Downloading...")
for local_name, file_url in links:
  if os.path.exists(os.path.dirname(local_name)) == False:
    os.makedirs(os.path.dirname(local_name))
  try:
    print("Loading: '{0}' to '{1}'".format(file_url,local_name))
    urllib.request.urlretrieve(file_url,local_name)
  except urllib.error.URLError as err:
    print(err)
    time.sleep(0.5)
    