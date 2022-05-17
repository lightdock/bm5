#!/bin/bash

COMPLEX=$1

# Setup
lightdock3_setup.py ${COMPLEX}_r_u.pdb ${COMPLEX}_l_u.pdb --noxt --noh -anm -anm_rec_rmsd 0.5 -anm_lig_rmsd 0.5

# Convert ANM files
python3 -c "import numpy as np; np.save('rec_nm.npy', np.load('lightdock_rec.nm.npy').flatten())"
python3 -c "import numpy as np; np.save('lig_nm.npy', np.load('lightdock_lig.nm.npy').flatten())"

# Prepare simulation
s=`ls -d swarm_* | wc -l`
swarms=$((s-1))
for i in `seq 0 $swarms`;do echo "cd swarm_${i}; cp ../lightdock_${COMPLEX}_r_u.pdb .; cp ../lightdock_${COMPLEX}_l_u.pdb .;cp ../rec_nm.npy .;cp ../lig_nm.npy .; lightdock-rust ../setup.json ../init/initial_positions_${i}.dat 100 dfire; rm -rf lightdock_*.pdb *.npy;" >> task.list; done

