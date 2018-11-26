#!/usr/bin/python

import re
import sys

cssfiles  = []
htmlfiles = []
idpatt    = re.compile('id="([^"]+)"')
clpatt    = re.compile('class="([^"]+)"')
clselpatt = re.compile('\.([a-zA-Z0-9]+)')
idselpatt = re.compile('\#([a-zA-Z0-9;]+)')

for i in sys.argv[1:]:
    if i.endswith("css"):
        cssfiles.append(i)
    else:
        htmlfiles.append(i)

classes = set()
ids     = set()
for html in htmlfiles:
    f = open(html)
    for line in f:
        match = idpatt.findall(line)
        if match:
            for m in match:
                ids.add(m)
        match = clpatt.findall(line)
        if match:
            for m in match:
                classes.add(m)
    f.close()

for css in cssfiles:
    f = open(css)
    for line in f:
        match = clselpatt.findall(line)
        if match:
            for m in match:
                if m not in classes:
                    print("Unused class: " + m)
        match = idselpatt.findall(line)
        if match:
            for m in match:
                if m.endswith(';'):
                    continue
                if m not in ids:
                    print("Unused id: " + m)
    f.close()
