#!/usr/bin/env python3
import sys
import os


def capri_score(fnat, i_rmsd, l_rmsd, dockq):
    """Calculates acceptable solutions or better according to CAPRI criteria"""
    #if (fnat >= 0.1 and l_rmsd <= 10.0) or (fnat >= 0.1 and i_rmsd <= 4.0): return 1
    if dockq >= 0.23: return 1
    else: return 0


if __name__ == "__main__":

    if len(sys.argv[1:]) != 1:
        print("Usage: %s /path/to/lgd_clustered_rank.list" % sys.argv[0])
        raise SystemExit("Wrong arguments")

    # Ranking file. Tipically lgd_clustered_rank.list or lgd_filtered_rank.list
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        raise SystemExit("Error: {} file does not exist".format(file_path))

    with open(file_path) as handle:
        ranks = []
        for line in handle:
            line = line.rstrip(os.linesep)
            if line:
                ranks.append(line.strip().split())

        # Store the different ranks
        t1 = 0
        t5 = 0
        t10 = 0
        t20 = 0
        t50 = 0
        t100 = 0
        t200 = 0
        t400 = 0
        t500 = 0
        t600 = 0
        t700 = 0
        t800 = 0
        t900 = 0
        t1000 = 0
        hits = 0

        i = 1
        for rank in ranks:
            try:
                # Order of the different values in the rank file:
                fnat = float(rank[1])
                i_rmsd = float(rank[2])
                l_rmsd = float(rank[3])
                dockq = float(rank[4])

                score = capri_score(fnat, i_rmsd, l_rmsd, dockq)
                
                if i == 1: t1 += score
                if i <= 5: t5 += score
                if i <= 10: t10 += score
                if i <= 20: t20 += score
                if i <= 50: t50 += score
                if i <= 100: t100 += score
                if i <= 200: t200 += score
                if i <= 400: t400 += score
                if i <= 500: t500 += score
                if i <= 600: t600 += score
                if i <= 700: t700 += score
                if i <= 800: t800 += score
                if i <= 900: t900 += score
                if i <= 1000: t1000 += score
                hits += score
            except IndexError:
                pass
            i += 1

print(':'.join([str(t) for t in [t1, t5, t10, t20, t50, t100, t200, t400, t500, t600, t700, t800, t900, t1000, hits]]))

