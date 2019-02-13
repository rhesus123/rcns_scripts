#!/usr/bin/python3

import re
import sys

patientre = re.compile("[0-9]+")

for i in open(sys.argv[1]):
	fields = i.rstrip().split("\t")
	match = patientre.search(fields[0])
	if match:
		fields[1] = match[0]
	nohs = fields[0].replace("hs_", "")
	if nohs.startswith("A") or nohs.startswith("SC"):
		fields[2] = "subcutane"
	else:
		fields[2] = "deep_neck"

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
	print("\t".join(fields))
