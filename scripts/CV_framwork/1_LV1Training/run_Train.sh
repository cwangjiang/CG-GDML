#!/bin/bash

# create three folders

rm -r NPZs
rm -r SLURMs_Train
#rm -r PYs
#rm -r TRAJs

mkdir NPZs
mkdir SLURMs_Train
#mkdir PYs
#mkdir TRAJs

sigma1=
X=50

rm -r sgdml/tmp/

for i in $(seq 1 $X) # 1 to X is to train 1 to 2X models
do

cp myjob_Train.slurm SLURMs_Train/myjob_Train$i.slurm

sed -i '25s/batch/&'$((i*20-19))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '25s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '26s/batch/&'$((i*20-18))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '26s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '27s/batch/&'$((i*20-17))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '27s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '28s/batch/&'$((i*20-16))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '28s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '29s/batch/&'$((i*20-15))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '29s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '30s/batch/&'$((i*20-14))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '30s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '31s/batch/&'$((i*20-13))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '31s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '32s/batch/&'$((i*20-12))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '32s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '33s/batch/&'$((i*20-11))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '33s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '34s/batch/&'$((i*20-10))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '34s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '35s/batch/&'$((i*20-9))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '35s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '36s/batch/&'$((i*20-8))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '36s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '37s/batch/&'$((i*20-7))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '37s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '38s/batch/&'$((i*20-6))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '38s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '39s/batch/&'$((i*20-5))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '39s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '40s/batch/&'$((i*20-4))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '40s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '41s/batch/&'$((i*20-3))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '41s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '42s/batch/&'$((i*20-2))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '42s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '43s/batch/&'$((i*20-1))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '43s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '44s/batch/&'$((i*20))'/' SLURMs_Train/myjob_Train$i.slurm

sed -i '44s/-s /&'$sigma1'/' SLURMs_Train/myjob_Train$i.slurm

done

#exit 1

cd NPZs

for i in $(seq 1 $X)
do

sbatch ../SLURMs_Train/myjob_Train$i.slurm

done


exit 1


#create N slurm files in clurm, each slurm file execute .py file in py folder

# create N slurm .py in py, each .py create traj in traj folder



# sbatch myjob_run1.slurm

# sbatch myjob_run2.slurm

# sbatch myjob_run3.slurm