#!/usr/bin/python2.6
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import cgi
import sys, os
import re
import posixpath, ntpath, macpath      # for client paths
import uuid
import zipfile
import json
from hashids import Hashids
cgitb.enable()
from string import Template


try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

print "Content-Type: application/json;charset=utf-8"
print

fs = cgi.FieldStorage()
name = fs.getvalue('name')
color = fs.getvalue('color')
srs = fs.getvalue('srs')
formato = fs.getvalue('format')
geometry = fs.getvalue('geometry')
fileitem = fs['clientfile']

uploaddir = '/dades/serveis/cloudifier/'

filename = uuid.uuid4().int
hashids = Hashids(salt='geostarterscloudifier')
hashname = hashids.encrypt(filename)
filename = str(filename)

def tifMap():
    rasterMap('.tif')

def mrsidMap():
    rasterMap('.sid')

def jpgMap():
    rasterMap('.jpg')

def dxfMap():
    dxfdgnMap('.dxf')

def dgnMap():
    dxfdgnMap('.dgn')

def rasterMap(ext):
    if fileitem.filename.endswith('.zip'):
        uploadFile(fileitem, filename, '.zip')
    else:
        uploadFile(fileitem, filename, ext)

    templatefile = os.path.join(uploaddir, 'templates', 'raster.map')
    mapfile = os.path.join(uploaddir, filename + '.map')
    d = {}
    d.update(layerName=name)
    d.update(srs=srs)
    d.update(dataFileName=filename + ext)
    d.update(rutaMapfile=filename)
    createMapFile(templatefile, d, mapfile)
    resp = {'map':filename, 'hashname': hashname}
    print json.dumps(resp)

def dxfdgnMap(ext):
    if fileitem.filename.endswith('.zip'):
        uploadFile(fileitem, filename, '.zip')
    else:
        uploadFile(fileitem, filename, ext)

    templatefile = os.path.join(uploaddir, 'templates', 'dgn_dxf.map')
    mapfile = os.path.join(uploaddir, filename + '.map')
    d = {}
    d.update(layerName=name)
    d.update(srs=srs)
    d.update(dataFileName=filename + ext)
    d.update(rutaMapfile=filename)
    createMapFile(templatefile, d, mapfile)
    resp = {'map':filename, 'hashname': hashname}
    print json.dumps(resp)

def shpMap():
    ext = '.shp'
    if fileitem.filename.endswith('.zip'):
        uploadFile(fileitem, filename, '.zip')
    else:
        uploadFile(fileitem, filename, ext)

    if geometry == 'point':
        templatefile = os.path.join(uploaddir, 'templates', 'shp_point.map')
    elif geometry == 'line':
        templatefile = os.path.join(uploaddir, 'templates', 'shp_line.map')
    elif geometry == 'polygon':
        templatefile = os.path.join(uploaddir, 'templates', 'shp_polygon.map')
    mapfile = os.path.join(uploaddir, filename + '.map')
    d = {}
    d.update(layerName=name)
    d.update(srs=srs)
    d.update(dataFileName=filename + ext)
    d.update(rutaMapfile=filename)
    d.update(color=color)
    createMapFile(templatefile, d, mapfile)
    resp = {'map':filename, 'hashname': hashname}
    print json.dumps(resp)

def uploadFile(fileitem, filename, ext):
    simpleName = filename
    filename = os.path.join('dades', filename + ext)
    fout = file (os.path.join(uploaddir, filename), 'wb')
    while 1:
        chunk = fileitem.file.read(100000)
        if not chunk: break
        fout.write (chunk)
    fout.close()
    if ext == '.zip':
        fileZ = os.path.join(uploaddir, filename)
        unzipFile(fileZ, simpleName)

def unzipFile(fileZ, filename):
    fh = open(fileZ, 'rb')
    z = zipfile.ZipFile(fh)
    for zname in z.namelist():
        extension = os.path.splitext(zname)[1]
        zitem = z.read(zname)
        zfilename = os.path.join('dades', filename + extension)
        with open(os.path.join(uploaddir, zfilename), 'wb') as w:
            w.write(zitem)

def createMapFile(template, dirdades, outfile):
    with open(template, 'r') as f:
        read_data = f.read()
        t = Template(read_data)
        read_data = t.substitute(dirdades)
        with open(outfile, 'w') as w:
            w.write(read_data)

options = {
    'shp': shpMap,
    'tif': tifMap,
    'sid': mrsidMap,
    'dxf': dxfMap,
    'dgn': dgnMap,
    'jpg': jpgMap,
}

try:
	options[formato]()
except KeyError:
    resp = {'error':"Format no valid"}
    print json.dumps(resp)
