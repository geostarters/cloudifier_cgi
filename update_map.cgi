#!/usr/bin/python2.6
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import cgi
import sys, os
import json

print "Content-Type: application/json;charset=utf-8"
print

fs = cgi.FieldStorage()
filename = fs.getvalue('name')
uploaddir = '/dades/serveis/cloudifier/'
mapfile = os.path.join(uploaddir, filename + '.map')
dirdades = os.path.join(uploaddir,'dades')
for f in os.listdir(dirdades):
	if f.startswith(filename):
		os.utime(os.path.join(dirdades,f),None)

if os.path.isfile(mapfile):
    os.utime(mapfile,None)
    resp = {'status': 'OK', 'update': filename}
    print json.dumps(resp)
else:
    resp = {'status': 'ERROR', 'update': filename}
    print json.dumps(resp)