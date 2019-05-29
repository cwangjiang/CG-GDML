#!/bin/bash

ID=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24)
# ID=(1 2 3 5 6 7 8 9 10)

stage=1
#stage=2


####### 1

x=$(squeue -u jw108 | wc -l)

while [ $x -ne 1 ]
do
sleep 600s
date +"%T"
x=$(squeue -u jw108 | wc -l)
echo "Remaining:"$x
done

for i in $(seq 1 10)
do

cd ${stage}_${ID[i-1]}/1_LV1Training/

./run_Train.sh

cd ../..

done

####### 2

sleep 10s

x=$(squeue -u jw108 | wc -l)

while [ $x -ne 1 ]
do
sleep 600s
date +"%T"
x=$(squeue -u jw108 | wc -l)
echo "Remaining:"$x
done


for i in $(seq 1 10)
do


cd ${stage}_${ID[i-1]}/2_Meanset/

./run_Predict.sh

# sbatch myjob_Meanset.slurm

cd ../..

done


####### 3

sleep 10s

x=$(squeue -u jw108 | wc -l)

while [ $x -ne 1 ]
do
sleep 60s
date +"%T"
x=$(squeue -u jw108 | wc -l)
echo "Remaining:"$x
done


for i in $(seq 1 10)
do


cd ${stage}_${ID[i-1]}/2_Meanset/

# ./run_Predict.sh

sbatch myjob_Meanset.slurm


cd ../..

done


####### 4

sleep 10s

x=$(squeue -u jw108 | wc -l)

while [ $x -ne 1 ]
do
sleep 60s
date +"%T"
x=$(squeue -u jw108 | wc -l)
echo "Remaining:"$x
done


for i in $(seq 1 10)
do

cd ${stage}_${ID[i-1]}/3_LV2Training

./run_Train.sh

cd ../..

done



####### 5

sleep 10s

x=$(squeue -u jw108 | wc -l)

while [ $x -ne 1 ]
do
sleep 600s
date +"%T"
x=$(squeue -u jw108 | wc -l)
echo "Remaining:"$x
done


for i in $(seq 1 10)
do


cd ${stage}_${ID[i-1]}/4_Validation

./run_Valid.sh

# sbatch myjob_CV.slurm


cd ../..

done


####### 6

sleep 10s

x=$(squeue -u jw108 | wc -l)

while [ $x -ne 1 ]
do
sleep 60s
date +"%T"
x=$(squeue -u jw108 | wc -l)
echo "Remaining:"$x
done


for i in $(seq 1 10)
do

cd ${stage}_${ID[i-1]}/4_Validation

# ./run_Valid.sh

sbatch myjob_CV.slurm


cd ../..

done