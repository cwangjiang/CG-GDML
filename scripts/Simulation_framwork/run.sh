#!/bin/bash

# create three folders


rm -r SLURMs
rm -r PYs
rm -r TRAJs


mkdir SLURMs
mkdir PYs
mkdir TRAJs



for i in $(seq 1 100)
do

cp myjob_run.slurm SLURMs/myjob_run$i.slurm

sed -i 's/Simulation_6atom_/&'$i'/' SLURMs/myjob_run$i.slurm



cp Simulation_6atom.py PYs/Simulation_6atom_$i.py

sed -i 's/ID = /&'$i'/' PYs/Simulation_6atom_$i.py


done

cp -r sgdml PYs/

cd SLURMs

for i in $(seq 1 100)
do

sbatch myjob_run$i.slurm

done


exit 1


#create N slurm files in clurm, each slurm file execute .py file in py folder

# create N slurm .py in py, each .py create traj in traj folder



# sbatch myjob_run1.slurm

# sbatch myjob_run2.slurm

# sbatch myjob_run3.slurm