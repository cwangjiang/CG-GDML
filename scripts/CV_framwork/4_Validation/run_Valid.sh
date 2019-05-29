#!/bin/bash

# create three folders

rm -r PYs
rm -r SLURMs_valid
rm -r SqErs

mkdir PYs
mkdir SLURMs_valid
mkdir SqErs

cp -r sgdml PYs

for i in $(seq 1 5) # loop over 5 folds
do

for j in $(seq 1 10) # each fold have 100 parallel sections. 
do

cp myjob_Valid.slurm SLURMs_valid/myjob_Valid$i\_$j.slurm

sed -i 's/Compute_Valid/&'$i'_'$j'/' SLURMs_valid/myjob_Valid$i\_$j.slurm


cp Compute_Valid.py PYs/Compute_Valid$i\_$j.py

sed -i 's/foldID =/&'$i'/' PYs/Compute_Valid$i\_$j.py
sed -i 's/parallelID =/&'$j'/' PYs/Compute_Valid$i\_$j.py

done

done

#exit 1

cd SLURMs_valid

for i in $(seq 1 5) # loop over 5 folds
do

for j in $(seq 1 10) # each fold have 100 parallel sections. 
do

sbatch myjob_Valid$i\_$j.slurm

done

done


exit 1


#create N slurm files in clurm, each slurm file execute .py file in py folder

# create N slurm .py in py, each .py create traj in traj folder



# sbatch myjob_run1.slurm

# sbatch myjob_run2.slurm

# sbatch myjob_run3.slurm