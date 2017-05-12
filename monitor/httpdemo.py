#!/usr/bin/env python
#coding:utf8
import urllib
import socket
#socket.setdefaulttimeout(1)
#k=urllib.urlopen('https://www.elastic.co/')
#print k.readlines()
#k.close()
import urllib2
response = urllib2.urlopen('http://192.168.57.98:9201', timeout=10)
print response.readlines()
response.close()
