#!/usr/bin/env python3

import sys
import os

csv_file = sys.argv[1]
tops = {1:0, 5:0, 10:0, 20:0, 50:0, 100:0, 200:0, 400:0, 500:0, 600:0, 700:0, 800:0, 900:0, 1000:0}
hits = 0

def top(value):
    if int(value) > 0:
        return 1
    return 0

total = 0
with open(csv_file) as ih:
    # 1F34:0:0:0:1:1:1:2:2:2:2:2:2:2:2:2
    for line in ih:
        line = line.rstrip(os.linesep)
        field = line.split(':')
        tops[1] += top(field[1])
        tops[5] += top(field[2])
        tops[10] += top(field[3])
        tops[20] += top(field[4])
        tops[50] += top(field[5])
        tops[100] += top(field[6])
        tops[200] += top(field[7])
        tops[400] += top(field[8])
        tops[500] += top(field[9])
        tops[600] += top(field[10])
        tops[700] += top(field[11])
        tops[800] += top(field[12])    
        tops[900] += top(field[13])
        tops[1000] += top(field[14])
        hits += top(field[15])
        total += 1

for k in sorted(tops.keys()):
    print(f"Top {k}: {float(tops[k])/total*100:.2f}%")

print(f"Hits: {float(hits)/total*100:.2f}%")

