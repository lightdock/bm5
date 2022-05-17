#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Please provide a PDB ID"
    exit 1
fi

COMPLEX=$1
CORES=126

### Clean up the house before starting ###
rm -rf generate_lightdock.list cluster_lightdock.list calculate_dockq.list;
rm -rf swarm_*/*.pdb;
rm -rf swarm_*/cluster.repr;

### Number of swarms ###
s=`ls -d swarm_* | wc -l`
swarms=$((s-1))

### Create files ###

for i in $(seq 0 $swarms)
  do
    echo "cd swarm_${i}; lgd_generate_conformations.py ../${COMPLEX}_r_u.pdb ../${COMPLEX}_l_u.pdb  gso_100.out 200 --setup ../setup.json > /dev/null 2> /dev/null;" >> generate_lightdock.list;
  done

for i in $(seq 0 $swarms)
  do
    echo "cd swarm_${i}; lgd_cluster_bsas.py gso_100.out > /dev/null 2> /dev/null;" >> cluster_lightdock.list;
  done

### Generate LightDock models ###
ant_thony.py -c ${CORES} generate_lightdock.list;

### Cluster structures ###

ant_thony.py -c ${CORES} cluster_lightdock.list;

### Generate ranking files ###

lgd_rank.py $s 100;

### Copy structures to be analyzed ###

lgd_copy_structures.py rank_by_scoring.list > /dev/null 2> /dev/null;

### Calculate DockQ ###
cd clustered;
ls *.pdb > pdbs.list;
for pdb in `cat pdbs.list`
  do
    echo "/opt/science/DockQ/DockQ.py ${pdb} ../${COMPLEX}_segid.pdb -short > ${pdb}.dockq" >> calculate_dockq.list;
  done

ant_thony.py -c ${CORES} calculate_dockq.list;

cd ../;
echo "${COMPLEX} analysis done. Go drink something."

