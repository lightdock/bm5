#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Please provide a PDB ID"
    exit 1
fi

COMPLEX=$1

cd $COMPLEX;

### Number of swarms ###
s=`ls -d swarm_* | wc -l`
swarms=$((s-1))

for i in $(seq 0 $swarms)
  do
    rm -rf swarm_${i}/*.pdb;
  done

cd ..;

echo "${COMPLEX} cleaning: Done."
