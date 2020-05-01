
import numpy as np

from io import StringIO
import csv


log = []
with open('server.log', "r") as file:
	for line in file.readlines():
	    log.append(line.rstrip())

si = StringIO()
cw = csv.writer(si)
cw.writerows(log)

print(cw)