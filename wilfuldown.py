#!/usr/bin/python3

"""
   This downloader is wilful, retry downloading stuff from TCGA until success
"""

import sys
import os
import time

manifest = open(sys.argv[1])
header   = manifest.readline()

for i in manifest:
    record  = i

    outmani = open("tmp.mani", "w")
    outmani.write(header)
    outmani.write(record)
    outmani.close()

    for retry in range(100):
        os.system("gdc-client download -d snps/ -m tmp.mani -t ~/Downloads/gdc-user-token.2017-10-04T09_38_47.351Z.txt --retry-amount 100 --wait-time 10 --log-file tmp.log >/dev/null")
        log = open("tmp.log")
        failed = 0
        for j in log:
            if "Failed downloads" in j:
                failed = int(j.split()[5])
        log.close()
        os.system("rm tmp.log")
        if failed == 0:
            break
        time.sleep(10)
        print(".", end = "", flush = True)
    print()
