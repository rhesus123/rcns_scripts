#!/usr/bin/python3

"""
   Simpel script to convert all the publication XML files to a text corpus
"""

import re
import sys
from xml.dom import minidom
import glob
import gzip

xmltags  = re.compile("<[^>]+>")
nonalpha = re.compile("[.,-?!+%]")
numbers  = re.compile(" \d+ ")

for f in glob.glob("*.xml.gz"):
    myxml = minidom.parse(gzip.open(f))
    textbody = myxml.getElementsByTagName("body")
    for chunk in textbody:
        notags = xmltags.sub("", chunk.toxml())
        nobreak = notags.replace("\n", "")
        nomarks = nonalpha.sub("", nobreak)
        nonum   = numbers.sub(" ", nomarks)
        rawtext = nonum.lower()
        rawtext = rawtext.replace(" the ", " ")
        rawtext = rawtext.replace(" of ", " ")
        rawtext = rawtext.replace(" for ", " ")
        rawtext = rawtext.replace(" has ", " ")
        rawtext = rawtext.replace(" by ", " ")
        rawtext = rawtext.replace(" in ", " ")
        rawtext = rawtext.replace(" to ", " ")
        rawtext = rawtext.replace(" from", " ")
        rawtext = rawtext.replace(" a ", " ")
        rawtext = rawtext.replace(" an ", " ")
        rawtext = rawtext.replace(" and ", " ")
        rawtext = rawtext.replace(" is ", " ")
        rawtext = rawtext.replace(" were ", " ")
        rawtext = rawtext.replace(" as ", " ")
        print(rawtext)
    print(f, file=sys.stderr)
