#!/bin/bash
#SBATCH --job-name=Simulation
#SBATCH --account=commons
#SBATCH --partition=commons
##SBATCH --partition=serial_long
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=10G
#SBATCH --time=8:00:00
##SBATCH --mail-user=cwjiang1989@gmail.com
##SBATCH --mail-type=ALL

# touch test.txt
# echo 'abcd' >> test.txt

module load Anaconda3/5.0.0
source activate py27

srun python ../PYs/Simulation_6atom_.py

#srun python Simulation_6atom.py >> log.txt

# echo "My job ran on:"
# echo $SLURM_NODELIST
# if [[ -d $SHARED_SCRATCH/$USER && -w $SHARED_SCRATCH/$USER ]]
# then
#     cd $SHARED_SCRATCH/$USER
#     srun /path/to/myprogram
# fi