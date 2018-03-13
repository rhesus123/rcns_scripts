#!/usr/bin/python3

"""
   Simpel script to convert all the publication XML files to a text corpus
"""

import re
import sys
from xml.dom import minidom
import gzip

xmltags  = re.compile("<[^>]+>")
nonalpha = re.compile("[^a-zA-Z0-9]")
numbers  = re.compile(r"\b\d+\b")
blacklist = ["the", "of", "for", "has", "have", "had", "by", "be", "in", "to", "from", "a", "an", "and", "at", "is", "were", "as", "then", "that", "that", "these", "or", "are", "on", "was", "we", "with", "which", "can"]

myxml = minidom.parse(gzip.open(sys.argv[1]))
textbody = myxml.getElementsByTagName("body")
for chunk in textbody:
    notags = xmltags.sub("", chunk.toxml())
    nobreak = notags.replace("\n", "")
    nomarks = nonalpha.sub(" ", nobreak)
    nonum   = numbers.sub("", nomarks)
    rawtext = nonum.lower()
    for bl in blacklist:
        rawtext = rawtext.replace(" " + bl + " ", " ")
    print(rawtext)
