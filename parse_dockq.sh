#!/bin/bash

COMPLEX=$1

cd ${COMPLEX};
cd clustered;
rm -rf results.list;
for i in `awk '{print $1}' rank_clustered.list`;do echo -ne "$i  "; awk '{print $4 "  " $6 "  " $8 "  " $2}' ${i}.dockq; done >> results.list
cd ..;
cd ..;

echo "${COMPLEX}/clustered/results.list"
