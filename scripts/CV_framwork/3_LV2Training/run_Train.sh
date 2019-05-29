#!/bin/bash

# create three folders

rm -r sgdml/tmp/

rm slurm-*
rm Meanset*


sed -i '21s/t\/Meanset/&1/' myjob_Train.slurm
sed -i '22s/t\/Meanset/&2/' myjob_Train.slurm
sed -i '23s/t\/Meanset/&3/' myjob_Train.slurm
sed -i '24s/t\/Meanset/&4/' myjob_Train.slurm
sed -i '25s/t\/Meanset/&5/' myjob_Train.slurm


#exit 1

for i in $(seq 1 5)
do

rm Meanset$i-unknown-train2999-sym1.npz

done

sbatch myjob_Train.slurm


exit 1


#create N slurm files in clurm, each slurm file execute .py file in py folder

# create N slurm .py in py, each .py create traj in traj folder



# sbatch myjob_run1.slurm

# sbatch myjob_run2.slurm

# sbatch myjob_run3.slurm