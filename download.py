#!/usr/bin/env python3 
import conf
import urllib.request
import urllib.error
import os
import re
import time

def loadLinks(filename):
  links = set()
  try:
    fd = open(filename, "rt")
    for l in fd:
      links.add(l.strip())
    fd.close()
  except IOError as err:
    print(err)
  return links

def saveLinks(links, filename):
  fd = open(filename, "wt")
  for l in links:
    fd.write(l+"\n")
  fd.close()


#main  
#read config
print("Reading config...")
cfg = conf.readConfig("config.cfg")

print("Building list...")
links = set()
#check 
links.update(loadLinks("download.db"))
try:
  for line in open("download.info"):
    line.strip()
    r = re.compile(r"((/[\w\_\d]+){3}/[\w\.\_\-\+\:\d]+\.tar\.xz)")
    match = r.search(line)
    if match:
      link = match.group(1)
      links.add(link.strip())
  #save list(load+append+save)
  saveLinks(links, "download.db")
  os.remove("download.info")
except IOError as err:
  print(err)

print("Downloading...")
while (len(links) > 0):
  ##load links
  link = links.pop()
  links.add(link)
  try:
    if link == "":
      continue
    file_url = cfg.serv+link
    local_name = cfg.path+link
    if os.path.exists(os.path.dirname(local_name)) == False:
      os.makedirs(os.path.dirname(local_name))
    print("Loading: '{0}' to '{1}'".format(file_url,local_name))
    urllib.request.urlretrieve(file_url,local_name)
  except urllib.error.URLError as err:
    print(err)
    time.sleep(1)
  finally:
    links.remove(link)
    saveLinks(links, "download.db")
    