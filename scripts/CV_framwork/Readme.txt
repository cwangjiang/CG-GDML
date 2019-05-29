##########################################
1_LV1Training

 Modify run_Train.sh, change sigma1, and number of LV1 models, X jobs contain 2X models. X can be 50 or 500.

 run "./run_Train.sh" to create x jobs for training 2X models, each model is trained on 1k points, myjob_Train.slurm are in /SLURMs_Train, trained models.npz and job outputs are in NPZs, since I can't control the output file path, I can only enter this folder to execute .slurm, so the output files are here.


##########################################
2_Meanset

Modify Predict.py, change number of Meanset size N, number of LV1 models from 1_LV1Training Nm, path to LV1 models.

Modify run_Predict.sh, change number of jobs X, each job could handle 2 LV1 models's prediction.

./run_Predict.sh, this will create .slurm files, .py files, enter SLURMs_Predict, submit all jobs, output to /AccumulateForce



Modify Create_Meanset.py, change N, Nm, range for each fold, to comebine all parallel part for each fold. 

submit job: sbatch myjob_Meanset.slrum

Since we need to do prediction, there must be a /sgdml folder


##########################################
3_LV2Training

Modify myjob_Train.slurm, change sigma2 and number of points in the Meanset, 3999 is OK.

./run_Train.sh


##########################################
4_Validation

Modify Compute_Valid.py, change batch number, path to 5 models, valid sets, and output path.

modify run_Valid.sh, change number of parallel sections, 200/2=100 

./run_Valid.sh to run all validation.

Modify Compute_CV.py, change parallel section number.

sbatch myjob_CV.slurm, to compute final CV error.



##########################################
Simulation

Modify Simulation_6atom, change path to the model trained on Meanset. T, dt, frequency

Modify run.sh, change number of run jobs, usually 100 parallel runs.

./run.sh to create .slurms, .pys, enter SLURMs, and submit all jobs, output trajectories are in TRAJs.

Modify Compute_Torsion.py, change number of trajectories, usually 100

./myjob_Analysis.slurm to compute FE and bond/angle distributins. 

Since doing simulation require prediction of force, there needs /sgdml folder.






####################################################################################
Once the first hyper parameter (sigma1, sigma2) case is done, we can quickly generate the rest cases based on the 1st one. (not based on framework), Usually modify the frame works as the 1st case, and copy and modify the framwork.

*****************
1_LV1Training

Just change sigma1 in run_Train.sh
./run_Train.sh


*****************
2_Meanset

change Predict.py the path to LV1 models.
./run_Predict.sh
sbatch myjob_Meanset.slrum


*****************
3_LV2Training

change sigma2 in myjob_Train.slurm
./run_Train.sh

*****************
4_Validation

In Compute_Valid.py, Change path to 5 models and output.
./run_Valid.sh
sbatch myjob_CV.slurm




####################################################################################
All the above modification can be done with ./config.sh, just need to modify config.sh, but for different
model, need to modify the modelX for the CV_framework


####################################################################################
All the above could be done using ./createCase.sh, when generating all the cases, even no need for config.sh, and modify those parameters manually for each case. But I still need to change model name for the CV_framwork, and paths in 2_Meanset/Predict.py



####################################################################################
At the execution time, I don't need to manually go to each folder to do ./run or sbatch, Just need to modify Submission.sh, and execute onece. 




####################################################################################
Doing simulation:
./run.sh

Doing analysis:
In Compute_Torsion/

./run_Torsion.sh
sbatch Combine.slurm



####################################################################################
All the training can be done automatically by submission_ALL.sh, but need to be run in a new screen.