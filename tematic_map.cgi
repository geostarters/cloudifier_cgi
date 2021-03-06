#!/usr/bin/python2.6
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import cgi
import sys, os, codecs
import json
from string import Template
cgitb.enable()

reload(sys)  
sys.setdefaultencoding('utf8')

#constantes
ext = '.shp'
uploaddir = '/cloudifier/serveis/cloudifier/'

print "Content-Type: application/json;charset=utf-8"
print

def tematic_polygon():
    global classtem
    for tem in tematic:
        lb = {}
        if label:
            lb.update(labelColor=str(labelColor))
            labelstyle = tl.substitute(lb)
        else:
            labelstyle = ""
        tem.update(label=str(labelstyle))
        read_data = t.substitute(tem)
        classtem += read_data

def tematic_line():
    global classtem
    for tem in tematic:
        lb = {}
        if label:
            lb.update(labelColor=str(labelColor))
            labelstyle = tl.substitute(lb)
        else:
            labelstyle = ""
        tem.update(label=str(labelstyle))
        read_data = t.substitute(tem)
        classtem += read_data

def tematic_point():
    global classtem
    for tem in tematic:
        lb = {}
        if label:
            lb.update(labelColor=str(labelColor))
            labelstyle = tl.substitute(lb)
        else:
            labelstyle = ""
        tem.update(label=str(labelstyle))
        read_data = t.substitute(tem)
        classtem += read_data

#leemos parametros post
#UTF8Reader = codecs.getreader('utf8')
#sys.stdin = UTF8Reader(sys.stdin)

myjson = json.load(sys.stdin)

filename = myjson["mapfile"]
layerName = myjson["name"]
geometry = myjson["geometry"]
srs = myjson["srs"]
estil = myjson["estil"]

mapfile = os.path.join(uploaddir, filename + '.map')

camp = estil["camp"]
label = estil["label"]
labelColor = estil["labelColor"]
labelCamp = estil["labelCamp"]
tematic = estil["tematic"]

labelfile = os.path.join(uploaddir, 'templates', 'label.map')
outfile = os.path.join(uploaddir, filename + '.map')

if geometry == 'point':
    templatefile = os.path.join(uploaddir, 'templates', 'shp_point_tem.map')
    classfile = os.path.join(uploaddir, 'templates', 'class_point.map')
elif geometry == 'line':
    templatefile = os.path.join(uploaddir, 'templates', 'shp_line_tem.map')
    classfile = os.path.join(uploaddir, 'templates', 'class_line.map')
elif geometry == 'polygon':
    templatefile = os.path.join(uploaddir, 'templates', 'shp_polygon_tem.map')
    classfile = os.path.join(uploaddir, 'templates', 'class_polygon.map')

with open(classfile, 'r') as f:
    read_data = f.read()
    t = Template(read_data)

with open(labelfile, 'r') as f:
    read_data = f.read()
    tl = Template(read_data)

classtem = ""

if geometry == 'point':
    tematic_point()
elif geometry == 'line':
    tematic_line()
elif geometry == 'polygon':
    tematic_polygon()

d = {}
d.update(layerName=str(layerName))
d.update(srs=str(srs))
d.update(dataFileName=str(filename + ext))
d.update(rutaMapfile=str(filename))
d.update(camp=str(camp))
d.update(labelCamp=str(labelCamp))
d.update(estils=str(classtem))

with open(templatefile, 'r') as f2:
    read_data2 = f2.read()
    t2 = Template(read_data2)
    read_data2 = t2.substitute(d)
    with open(outfile, 'w') as w:
        w.write(read_data2)


resp = {'status': 'OK', 'update': filename}
print json.dumps(resp)