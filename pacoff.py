#!/usr/bin/env python3 
import urllib.request
import urllib.error
import os
import os.path
import sys
import re
import time
from collections import namedtuple

PACOFF_DB_NAME = "download.db"
PACOFF_INFO_NAME = "download.info"
PACOFF_CONF_NAME = "config.cfg"

Config = namedtuple("Config", "serv repos archs cutdir path")

def readConfig(filename):
  fd = open(filename,"rt")
  for lno, line in enumerate(fd):
    if lno == 0:  serv = line.rstrip()
    if lno == 1:  repos = line.split()
    if lno == 2:  archs = line.split()
    if lno == 3:  cutdir = line.rstrip()
    if lno == 4:  path = line.rstrip()
  fd.close()
  return Config(serv,repos,archs,cutdir,path)

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

def updateDb(links): #links = set(...)
  print("Building list...")
  #check 
  links.update(loadLinks(PACOFF_DB_NAME))
  saveLinks(links, PACOFF_DB_NAME)

def convertInfoToDb():
  links = set()
  try:
    if os.path.exists(PACOFF_INFO_NAME):
      for line in open(PACOFF_INFO_NAME):
        line.strip()
        r = re.compile(r"((/[\w\_\d]+){3}/[\w\.\_\-\+\:\d]+\.tar\.xz)")
        match = r.search(line)
        if match:
          link = match.group(1)
          links.add(link.strip())
      updateDb(links)
      os.remove(PACOFF_INFO_NAME)
  except IOError as err:
    print(err)
  
#from download.py
def download():
  #read config
  print("Reading config...")
  cfg = readConfig(PACOFF_CONF_NAME)

  convertInfoToDb()
  links = loadLinks(PACOFF_DB_NAME)
  err_count = 0
  print("Downloading...")
  while (len(links) > 0 and err_count < 15):
    ##load links
    link = links.pop()
    links.add(link)
    try:
      if link == "":
        continue
      file_url = cfg.serv+link
      local_name = cfg.path+link
      #local_name = re.sub(":","\:", local_name)
      if os.path.exists(os.path.dirname(local_name)) == False:
        os.makedirs(os.path.dirname(local_name))
      if os.path.exists(local_name):
        print("{0} exists!".format(local_name))
        links.remove(link)
        continue
      print("Loading: '{0}' to '{1}'".format(file_url,local_name))
      urllib.request.urlretrieve(file_url,local_name)
      urllib.request.urlcleanup()
    except (ValueError,urllib.error.URLError) as err:
      print(err)
      if os.path.exists(local_name):
        os.remove(local_name)
        print(local_name+" removed!")
      time.sleep(1)
      err_count += 1
    except IOError as err:
      print(err)
      print("Name '{0}' may be not allowed on FAT/NTFS partitions!".format(link))
      links.remove(link)
      open("error.db","at").write(link+"\n")
    else:
      links.remove(link)
    finally:
      saveLinks(links, PACOFF_DB_NAME)
  if err_count > 10: print ("Too much errors while downloading!")

def update(): #update repo headers, append links into db for download
  #read config
  print("Reading config...")
  cfg = readConfig(PACOFF_CONF_NAME)
  links=set()
  for repo in cfg.repos:
    for arch in cfg.archs:
      if repo == 'multilib' and arch == 'i686':
        continue
      link = "/{repo}/os/{arch}/{repo}".format(repo=repo,arch=arch)
      links.add(link+".db")
      links.add(link+".files")
      local_name = cfg.path+link+".db"
      if os.path.exists(local_name):
        os.remove(local_name)
        print(local_name+" removed!")
      local_name = cfg.path+link+".files"
      if os.path.exists(local_name):
        os.remove(local_name)
        print(local_name+" removed!")
  updateDb(links)
  
def upgrade():
  print("Running upgrade...")
  os.system("sudo pacman -Suyp > download.info")
  convertInfoToDb()
  
  
if __name__ == "__main__":
  if len(sys.argv) == 2:
    if sys.argv[1].lower() == 'update': 
      update()
      download()
    if sys.argv[1].lower() == 'upgrade': upgrade()
    if sys.argv[1].lower() == 'download': download()
    if sys.argv[1].lower() == 'run': print("'run' command under construction - but wrong usage!")
  elif len(sys.argv) > 2:
    if sys.argv[1].lower() == 'run': print("'run' command under construction")
  elif len(sys.argv) == 1:
    #print help
    print("usage: {0} update|upgrade|download|run 'pacman-command'\n"
          "update - adds repo-headers links into download-database\n"
          "upgrade - runs 'sudo pacman -Suyp command' and adds links in download-database\n"
          "download - download all files in download-database\n"
          #"run - "
          "'run' command under construction".format(sys.argv[0]))
