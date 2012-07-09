#!/usr/bin/env python3

#server = "ftp://mirror.yandex.ru/archlinux"
#repos = ("core","extra","community","multilib")
#archs = ("i686", "x86_64")
                        
#print("{serv}/{repo}/os/{arch}/{pkg}".format(
#            serv=server,
#            repo=repos[2],
#            arch=archs[1],
#            pkg="pkg.tar.xz"
#        )
#        )

from collections import namedtuple

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

#def test()
#  out = readConfig("config.cfg")
#  print (out.serv)
#  print (out.repos)
#  print (out.archs)
