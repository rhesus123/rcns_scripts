#!/usr/bin/python3

import sys
import os

coding = {'3':'noncodingexon', '6': 'nmd', '9':'noncoding', '10':'downstream', '12':'missense','14':'intron', '18':'synonymous', '26':'upstream', '27': '3utr', 'tsv':'tsv'}
cancer = {'13' : 'all','14' : 'aml','3'  : 'breast','12' : 'colon','2': 'headandneck','7':'kidneyrccc','11' : 'kidneychromophobe','9'  : 'kidneyrpcc','8' : 'lungadeno','10' : 'lungscc','15' : 'neuroblastoma','1' : 'ovarian','4' : 'prostate','5' : 'rectum','6' : 'melanoma'}
db = {'1':'tcga', '2':'metabric', '3':'target'}

pices  = sys.argv[1].split(".")
pices[1] = cancer[pices[1]]
pices[2] = db[pices[2]]
pices[3] = coding[pices[3]]
newname = ".".join(pices)
os.rename(sys.argv[1], newname)
