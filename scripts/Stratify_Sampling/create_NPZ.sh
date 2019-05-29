#!/bin/bash

# create three folders

rm -r NPZ

mkdir NPZ

cd NPZ

for i in $(seq 1 1000)
do

#if [ $i = 200 ]||[ $i = 400 ]||[ $i = 600 ]||[ $i = 800 ]; then
if [ $(($i % 100)) = 0 ]; then
	sleep 100s
fi

python ../dataset_from_noe.py ../TXT/batch$i.txt 

done

#mv batch* NPZ

exit 1


#create N slurm files in clurm, each slurm file execute .py file in py folder

# create N slurm .py in py, each .py create traj in traj folder



# sbatch myjob_run1.slurm

# sbatch myjob_run2.slurm

# sbatch myjob_run3.slurm