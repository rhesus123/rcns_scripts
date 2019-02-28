#!/usr/bin/python3

import re
import sys

patientre = re.compile("[0-9]+")

for i in open(sys.argv[1]):
        fields = i.rstrip().split("\t")
        fields.append("")
        fields.append("")
        fields.append("")
        fields.append("")
        match = patientre.search(fields[0])
        if match:
                fields[1] = match[0]
        nohs = fields[0].replace("hs_", "")
        if nohs.startswith("A") or nohs.startswith("SC"):
                fields[2] = "subcutane"
                fields[5] = "sc"
        else:
                fields[2] = "deep_neck"
                fields[5] = "dn"

        if "PA" in fields[0]:
                fields[3] = "pa"
        elif fields[0] .endswith("B"):
                fields[3] = "b"
        elif "BMP" in fields[0]:
                fields[3] = "w_bmp"
        elif "IR" in fields[0]:
                fields[3] = "w_ir"
        else:
                fields[3] = "w"
        fields[5] = fields[5] + fields[3]
        if fields[1] == "2" or fields[1] == "15" or fields[1] == "19":
                fields[4] = "2016"
        elif fields[1] == "31" or fields[1] == "33":
                fields[4] = "2017"
        else:
                fields[4] = "2019"
        if fields[1] == "15" or fields[1] == "22" or fields[1] == "33":
            fields[6] = "male"
        else:
            fields[6] = "female"
        if fields[1] == "2" or fields[1] == "33" or fields[1] == "26":
            fields[7] = "heterogen"
        elif fields[1] == "15" or fields[1] == "19" or fields[1] == "22":
            fields[7] = "positive"
        else:
            fields[7] = "negative"
        print("\t".join(fields))
