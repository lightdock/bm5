#!/usr/bin/env python3

import os
import sys


def parse_ranking(file_name):
    ranking = []
    with open(file_name) as ih:
        for line in ih:
            if line:
                line = line.rstrip(os.linesep)
                try:
                    pdb_file, scoring = line.split()
                    ranking.append(pdb_file)
                except:
                    pass
    return ranking


def parse_dockq_file(file_name):
    """DockQ short file looks like:
    
    DockQ 0.044 Fnat 0.067 iRMS 14.670 LRMS 34.874 Fnonnat 0.842 swarm_197_183.pdb ../1A2K_alt.pdb
    """
    with open(file_name) as ih:
        for line in ih:
            if line:
                line = line.rstrip(os.linesep)
                try:
                    fields = line.split()
                    dockq_score = float(fields[1])
                    fnat = float(fields[3])
                    irmsd = float(fields[5])
                    lrmsd = float(fields[7])
                    return dockq_score, irmsd, lrmsd, fnat 
                except:
                    raise SystemExit(f"Error: cannot parse line [{line}]")


if __name__ == "__main__":

    if len(sys.argv[1:]) != 3:
        raise SystemExit(f"Usage: {sys.argv[0]} ranking_file number_of_interfaces output_file")
    ranking_file = sys.argv[1]
    number_of_interfaces = int(sys.argv[2])
    output_file = sys.argv[3]

    ranking = parse_ranking(ranking_file)
    results = {}
    for structure in ranking:
        results[structure] = []
        print(structure)
        for i in range(number_of_interfaces):
            suffix = '.dockq'
            if i >= 1:
                suffix += str(i+1)
            dockq_file_name = f"{structure}{suffix}"
            dockq_score, irmsd, lrmsd, fnat = parse_dockq_file(dockq_file_name)
            results[structure].append([dockq_score, irmsd, lrmsd, fnat])

    with open(output_file, 'w') as oh:
        for structure in ranking:
            max_dockq = max([l[0] for l in results[structure]])
            min_irmsd = min([l[1] for l in results[structure]])
            min_lrmsd = min([l[2] for l in results[structure]])
            max_fnat = max([l[3] for l in results[structure]])
            oh.write(f"{structure}  {max_fnat}  {min_irmsd}  {min_lrmsd}  {max_dockq}{os.linesep}")

