#!/bin/bash

# create three folders


rm -r SLURM_Torsions
rm -r PYs
rm -r Torsions


mkdir SLURM_Torsions
mkdir PYs
mkdir Torsions



for i in $(seq 1 100)
do

cp myjob_Torsion.slurm SLURM_Torsions/myjob_Torsion$i.slurm

sed -i 's/Compute_Torsion/&'$i'/' SLURM_Torsions/myjob_Torsion$i.slurm



cp Compute_Torsion.py PYs/Compute_Torsion$i.py

sed -i 's/ID =/&'$i'/' PYs/Compute_Torsion$i.py


done

#cp -r sgdml PYs/

cd SLURM_Torsions

for i in $(seq 1 100)
do

sbatch myjob_Torsion$i.slurm

done


exit 1


#create N slurm files in clurm, each slurm file execute .py file in py folder

# create N slurm .py in py, each .py create traj in traj folder



# sbatch myjob_run1.slurm

# sbatch myjob_run2.slurm

# sbatch myjob_run3.slurm