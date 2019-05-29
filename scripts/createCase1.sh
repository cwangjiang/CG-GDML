 #!/bin/bash

Sig=(70 80 90 100 150 200 250 300 350 400 450 500 550 600 650 700 750 800 850)
#lambda=(0 1e-20 1e-19 1e-18 1e-17 1e-16 1e-15 1e-14 1e-13 1e-12)

# path to 1k by 1k traning/validation set
path1='NPZ1'
# path to 3k mean force set
path2='coordforce_6atom_Uniform_3k_b300'




for i in $(seq 1 10)
do

cp -r CV_framwork 1_$i

cd 1_$i

sed -i 's/6_atom\//&'$path1'/' 1_LV1Training/myjob_Train.slurm
sed -i 's/6_atom\//&'$path2'/' 2_Meanset/Predict.py
sed -i 's/6_atom\//&'$path2'/' 2_Meanset/Create_Meanset.py
sed -i 's/6_atom\//&'$path1'/' 4_Validation/Compute_Valid.py



sigma1=${Sig[i-1]}
# sigma1=320

sed -i 's/sigma1=/&'$sigma1'/' 1_LV1Training/run_Train.sh

lambda=1e-15

sed -i '177s/lam = 1e-15/lam = '$lambda'/' 1_LV1Training/sgdml/cli.py

# 2_Meanset change Predict.py the path to LV1 models.

# sed -i 's/model24\//&1_'$i'/' 2_Meanset/Predict.py


# 3_LV2Training  change sigma2 in myjob_Train.slurm
sigma2=40

sed -i 's/-s /&'$sigma2'/' 3_LV2Training/myjob_Train.slurm


# 4_Validation In Compute_Valid.py, Change path to 5 models and output.

# sed -i 's/model24\//&1_'$i'/' 4_Validation/Compute_Valid.py


cd ..

done

exit 1









