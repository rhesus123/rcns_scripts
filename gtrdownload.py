#!/usr/bin/python3

import sys
import urllib.request
from xml.dom import minidom

def download(url):
    response = urllib.request.urlopen(url).read()
    xml      = minidom.parseString(response)
    return(xml)

term = sys.argv[1]

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
    for analyte in analytes:
        genename = analyte.getElementsByTagName("Name")[0].childNodes[0].data
        location = analyte.getElementsByTagName("Location")[0].childNodes[0].data
        #print(testname, offerer, genename, location, sep = "\t")
    cond     = "https://www.ncbi.nlm.nih.gov/gtr/tests/" + gtestid + "/methodology/"
    xml2     = download(cond)
    table    = xml2.getElementsByTagName("table")[0]
    print(table)
