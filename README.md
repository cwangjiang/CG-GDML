# CG-GDML_script

This repository contains the basic script for training 2-layer GDML model for the purpose of coars graining the alanine-dipeptide.

## Stratify_Sampling
Sample 1000 points for training batches for the 1st-layer model, and sample 1000 batches, the sampling is conducted uniformly over the phi,psi torsion space of dialanine. Then sample 3000 point for the 2nd-layer model. During the sampling the 1st-layer, we can choose to whether subtract the original force with the computed prior force.

## CV_framwork
Training a 2-layer model for a giving sigma1 and sigma2.

1_LV1Training, training 1000 1st-layer model.

2_Meanset, predict force for the mean force set using the trained 1000 models, compute the mean force and generate the mean force set.

3_LV2Training, Training 5 fold 2nd-layer models.

4_Validation, Compute the validation error.

## Simulation_framwork
Simulate the trained 1nd-layer model using overdamped Langevin dynamics, and compute the torsion and free energy surface of the simulated CG alanine-dipepdite.

## createCase1.sh createCase2.sh
Generate initial training files for 2 stages with different sigma1, sigma2 values.

## Submission_ALL1.sh Submission_ALL2.sh
Submit the training for different sigma1, sigma2 automatically.