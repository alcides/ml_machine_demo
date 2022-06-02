#!/bin/bash
#SBATCH --job-name=ppc_a1      # Job name
#SBATCH --nodes=1                    # Run all processes on a single node	
#SBATCH --ntasks=1                   # Run a single task		
#SBATCH --cpus-per-task=1            # Number of CPU cores per task
#SBATCH --mem=1gb                    # Job memory request
#SBATCH --time=00:02:00              # Time limit hrs:min:sec
#SBATCH --output=parallel_%j.log     # Standard output and error log
#SBATCH --gres=gpu:1

#SBATCH --array=0-59                # iterate values between 0 and 59, inclusive

bash setup.sh
python3 example.py -s $(expr $SLURM_ARRAY_TASK_ID / 2) -m $(expr $SLURM_ARRAY_TASK_ID % 2)