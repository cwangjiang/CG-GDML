#!/bin/bash

#1_LV1Training Just change sigma1 in run_Train.sh
sigma1=10

sed -i 's/sigma1=/&'$sigma1'/' 1_LV1Training/run_Train.sh


# 2_Meanset change Predict.py the path to LV1 models.

sed -i 's/model20\//&1_1/' 2_Meanset/Predict.py


# 3_LV2Training  change sigma2 in myjob_Train.slurm
sigma2=480

sed -i 's/-s /&'$sigma2'/' 2_Meanset/Predict.py


# 4_Validation In Compute_Valid.py, Change path to 5 models and output.

sed -i 's/model20\//&1_1/' 4_Validation/Compute_Valid.py





