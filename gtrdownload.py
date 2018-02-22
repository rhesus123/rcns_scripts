#!/usr/bin/python3

"""
   Script to download genes and conditions from NCBI's GTR website
   The input parameter is the ID of the condition. For example for
   medulloblastoma one can use the following command line:
   python3 gtrdownload.py C0025149
   The output is the test, the affected gene, condition and the offerer of the test
"""

import sys
import urllib.request
import re
from xml.dom import minidom

def download(url):
    response = urllib.request.urlopen(url).read()
    xml      = minidom.parseString(response)
    return(xml)

term = sys.argv[1]
pattern = re.compile("<[^>]+>")
newline = re.compile("<br/>")
whitesp = re.compile("\s+")

tests = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gtr&term=" + term + "&retstart=0&retmax=300" # later we will made it more appropriate
xml = download(tests)

ids = xml.getElementsByTagName("Id")
for i in ids:
    gtestid  = i.childNodes[0].data
    gtesturl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gtr&id=" + gtestid
    xml2     = download(gtesturl)
    testname = xml2.getElementsByTagName("TestName")[0].childNodes[0].data
    offerer  = xml2.getElementsByTagName("Offerer")[0].childNodes[0].data
    analytes = xml2.getElementsByTagName("Analyte")
    cond     = "https://www.ncbi.nlm.nih.gov/gtr/tests/" + gtestid + "/methodology/"
    xml2     = download(cond)
    table    = xml2.getElementsByTagName("tbody")[0]
    rows     = table.getElementsByTagName("tr")
    for row in rows:
        columns = row.getElementsByTagName("td")
        first   = pattern.sub(" ", columns[0].toxml())
        last    = newline.sub("|", columns[-1].toxml())
        last    = pattern.sub(" ", last)
        last    = whitesp.sub(" ", last)
        print(testname, first, last, offerer, sep = "\t")
