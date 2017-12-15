#!/usr/bin/python3

import sys

f = open(sys.argv[1])
f.readline()
print("tumor_stage\tage_at_diagnosis\tdays_to_deathorfollowup\tdead\trace\tgender")
for i in f:
    fields = i.rstrip().split("\t")
    if fields[3] == "NA":
        fields[3] = "0"
    if fields[4] == "NA":
        fields[4] = "0"
    day = max(float(fields[3]), float(fields[4]))
    print("\t".join(fields[:3]) + "\t" + str(day) + "\t" + "\t".join(fields[5:]))
