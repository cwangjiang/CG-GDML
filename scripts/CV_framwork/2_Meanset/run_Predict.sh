#!/bin/bash

# create three folders

rm -r AccumulateForce
rm -r SLURMs_Predict
rm -r PYs
#rm -r TRAJs

mkdir AccumulateForce
mkdir SLURMs_Predict
mkdir PYs
#mkdir TRAJs

X=50

for i in $(seq 1 $X) # 1 to X is to train 1 to 10X models
do

cp myjob_Predict.slurm SLURMs_Predict/myjob_Predict$i.slurm

sed -i 's/Predict/&'$i'/' SLURMs_Predict/myjob_Predict$i.slurm

cp Predict.py PYs/Predict$i.py

sed -i '16s/arange(/&'$((i*20-20))','$((i*20))'/' PYs/Predict$i.py
sed -i '40s/str(/&'$i'/' PYs/Predict$i.py

done

cp -r sgdml PYs/

#exit 1

cd SLURMs_Predict

for i in $(seq 1 $X)
do

sbatch myjob_Predict$i.slurm

done


exit 1


#create N slurm files in clurm, each slurm file execute .py file in py folder

# create N slurm .py in py, each .py create traj in traj folder



# sbatch myjob_run1.slurm

# sbatch myjob_run2.slurm

# sbatch myjob_run3.slurm