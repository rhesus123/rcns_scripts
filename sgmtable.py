#!/usr/bin/python3

"""
   Sample-gene-mutation table generation tool
"""

import sys
import gzip
import re
import os

veppatt = re.compile("CSQ=([^;]+)")

samplename = sys.argv[1]

sampleid = os.path.basename(samplename.replace(".vep.vcf.gz", ""))

for i in gzip.open(samplename, "rt"):
    if i.startswith("#"):
        continue
    fields = i.rstrip().split()
    match = veppatt.search(fields[7])
    if match:
        vepannot = match.group(1)
        for veprec in vepannot.split(","):

            vepfields    = veprec.split("|")
            consequences = vepfields[1]
            symbol       = vepfields[3]
            ensid        = vepfields[4]

            for cons in consequences.split("&"):
                print(sampleid, cons, symbol, ensid, sep = "\t")
