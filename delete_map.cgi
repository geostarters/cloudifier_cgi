#!/usr/bin/python2.6
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import cgi
import sys, os
import uuid
import json
from hashids import Hashids

print "Content-Type: application/json;charset=utf-8"
print

fs = cgi.FieldStorage()
name = fs.getvalue('name')
uploaddir = '/dades/serveis/cloudifier/'
hashids = Hashids(salt='geostarterscloudifier')

numbers = hashids.decrypt(name)
hashname = numbers[0]
filename = str(hashname)

mapfile = os.path.join(uploaddir, filename + '.map')
dirdades = os.path.join(uploaddir,'dades')
for f in os.listdir(dirdades):
	if f.startswith(filename):
		os.remove(os.path.join(dirdades,f))

if os.path.isfile(mapfile):
    os.remove(mapfile)
    resp = {'status': 'OK', 'delete': filename}
    print json.dumps(resp)
else:
    resp = {'status': 'ERROR', 'delete': filename}
    print json.dumps(resp)