#!/bin/bash
#SBATCH --job-name=LV1Training
#SBATCH --account=commons
#SBATCH --partition=commons
##SBATCH --partition=serial_long
##SBATCH --cpus-per-task=8
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=10G
#SBATCH --time=8:00:00
##SBATCH --mail-user=cwjiang1989@gmail.com
##SBATCH --mail-type=ALL

# touch test.txt
# echo 'abcd' >> test.txt

module load Anaconda3/5.0.0
source activate py27

# rm -r BondAngle
# mkdir BondAngle

#cd release/sgdml/
#srun python release/sgdml/cli.py all /scratch/jw108/model18/coordforce_6atom_4500random.npz 1000 10 10 -s 1000 --gdml 

srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 
srun python ../sgdml/cli.py all /scratch/jw108/Dialanine_data/6_atom//batch.npz 999 1 1 -s  --gdml 

#srun python Simulation_6atom.py >> log.txt

# echo "My job ran on:"
# echo $SLURM_NODELIST
# if [[ -d $SHARED_SCRATCH/$USER && -w $SHARED_SCRATCH/$USER ]]
# then
#     cd $SHARED_SCRATCH/$USER
#     srun /path/to/myprogram
# fi