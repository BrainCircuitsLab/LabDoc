#!/bin/bash

# simple SLURM script for submitting jobs.

#----------------------------------------

# setup parameters

#SBATCH -J launcher
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -p TVB
#SBATCH -o job.%j.out
#SBATCH -e job.%j.err
#SBATCH -t 2-00:00:00

module load launcher

export LD_LIBRARY_PATH=/lib64:$LD_LIBRARY_PATH
export LAUNCHER_WORKDIR=$HOME/workdir
export LAUNCHER_JOB_FILE=jobfile

$LAUNCHER_DIR/paramrun