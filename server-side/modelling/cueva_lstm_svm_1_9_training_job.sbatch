#!/bin/bash
#SBATCH --account=pup-manila    
#SBATCH --partition=batch
#SBATCH --qos=batch_default
##SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --job-name="cueva_lstm_svm_1_9_training_job"
#SBATCH --output="%x.out"         ## <jobname>.<jobid>.out
##SBATCH --mail-type=ALL          ## optional
##SBATCH --mail-user=<email_add>  ## optional
##SBATCH --requeue                ## optional
##SBATCH --ntasks-per-node=1      ## optional
#SBATCH --mem=200G                ## optional: mem per node
##SBATCH --error="%x.%j.err"      ## optional; better to use --output only

## For more `sbatch` options, use `man sbatch` in the HPC, or go to https://slurm.schedmd.com/sbatch.html.

## Set stack size to unlimited.
ulimit -s unlimited

## Benchmarking.
start_time=$(date +%s.%N)

## Print job parameters.
echo "Submitted on $(date)"
echo "JOB PARAMETERS"
echo "SLURM_JOB_ID          : ${SLURM_JOB_ID}"
echo "SLURM_JOB_NAME        : ${SLURM_JOB_NAME}"
echo "SLURM_JOB_NUM_NODES   : ${SLURM_JOB_NUM_NODES}"
echo "SLURM_JOB_NODELIST    : ${SLURM_JOB_NODELIST}"
echo "SLURM_NTASKS          : ${SLURM_NTASKS}"
echo "SLURM_NTASKS_PER_NODE : ${SLURM_NTASKS_PER_NODE}"
echo "SLURM_MEM_PER_NODE    : ${SLURM_MEM_PER_NODE}"

## Create a unique temporary folder in the node. Using a local temporary folder usually results in faster read/write for temporary files.
custom_tmpdir="yes"

if [[ $custom_tmpdir == "yes" ]]; then
   JOB_TMPDIR=/tmp/${USER}/SLURM_JOB_ID/${SLURM_JOB_ID}
   mkdir -p ${JOB_TMPDIR}
   export TMPDIR=${JOB_TMPDIR}
   echo "TMPDIR                : $TMPDIR"
fi

## Reset modules.
module purge
module load anaconda/3-2023.07-2


## Main job. Run your codes, commands, and executables here; `srun` is optional.
conda activate thesis-writing-1
python --version
python tuning_ml.py -m svm -pl cueva_second_phase --mode training --hyper_param_list C_10 gamma_0.1 probability_True --inc_class_weight --comp_type my-balanced

## Flush the TMPDIR.
if [[ $custom_tmp == "yes" ]]; then
   rm -rf $TMPDIR
   echo "Cleared the TMPDIR (${TMPDIR})"
fi

## Benchmarking
end_time=$(date +%s.%N)
echo "Finished on $(date)"
run_time=$(python -c "print($end_time - $start_time)")
echo "Total runtime (sec): ${run_time}"
