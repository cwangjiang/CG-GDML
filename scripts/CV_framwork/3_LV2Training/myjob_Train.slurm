#!/bin/bash
#SBATCH --job-name=LV2Training
#SBATCH --account=commons
#SBATCH --partition=commons
##SBATCH --partition=serial_long
#SBATCH --cpus-per-task=4
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=20G
#SBATCH --time=8:00:00
##SBATCH --mail-user=cwjiang1989@gmail.com
##SBATCH --mail-type=ALL

# touch test.txt
# echo 'abcd' >> test.txt

module load Anaconda3/5.0.0
source activate py27


#cd release/sgdml/
srun python sgdml/cli.py all ../2_Meanset/Meanset.npz 2999 1 1 -s  --gdml 
srun python sgdml/cli.py all ../2_Meanset/Meanset.npz 2999 1 1 -s  --gdml 
srun python sgdml/cli.py all ../2_Meanset/Meanset.npz 2999 1 1 -s  --gdml 
srun python sgdml/cli.py all ../2_Meanset/Meanset.npz 2999 1 1 -s  --gdml 
srun python sgdml/cli.py all ../2_Meanset/Meanset.npz 2999 1 1 -s  --gdml 

# srun python release/sgdml/cli.py all /home/jw108/Remount_Davinci/GDML/sGDML-master/Training_set/coordforce_6atom_4579uniform.npz 4000 10 10 -s 80500 --gdml 

#srun python Simulation_6atom.py >> log.txt

# echo "My job ran on:"
# echo $SLURM_NODELIST
# if [[ -d $SHARED_SCRATCH/$USER && -w $SHARED_SCRATCH/$USER ]]
# then
#     cd $SHARED_SCRATCH/$USER
#     srun /path/to/myprogram
# fi