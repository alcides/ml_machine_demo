# DI_FCUL Computing Cluster

The [Department of Informatics](https://www.di.fc.ul.pt) of [Faculdade de Ciências da Universidade de Lisboa](http://ciencias.ulisboa.pt) has a computing cluster that staff can use to run experiments.


## Nodes

The cluster uses SLURM to control the execution of jobs. Users log into "login-node" to submit jobs. Those jobs are queued in SLURM and are executed by the following nodes, whenever the necessary resources are available.

### Opel

2x AMD EPYC 7443 24-Core Processor (96 hyper-threads total)
128GB RAM
6x NVIDIA A30 (24GB VRAM)

### Corsa

2x Intel(R) Xeon(R) Silver 4216 CPU @ 2.10GHz (64 hyper-threads total)
128GB RAM
2x NVIDIA Tesla T4 (16GB VRAM)


## Software

OS: Ubuntu 24.04
SLURM: 23.11
CUDA: 12.0


# How to use the cluster

1. Run `$EDITOR .ssh/config`

Add the following configuration:

```config
Host ml
HostName login-node.di.fc.ul.pt
User <username>@lasige.difc.ul.pt
```

Remove `lasige.` if you are a professor.

2. Upload the files in the current folder to the server folder.

`scp -r ../ml_machine_demo ml:`

3. Remotely login into the `login-node`

`ssh ml`

You are now in the server.

4. Submit the job to the server.

```bash
cd machine_learning_demo
sbatch run.sh
```

You always need to submit a bash job, where different parameters are set.

5. Monitor the progress

`squeue`

6. From your original machine, download all generated files.

`scp -r ml:machine_learning_demo/* .`

# Understanding SLURM parameters

```sh
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

curl -LsSf https://astral.sh/uv/install.sh | sh

uv run --with tensorflow python example.py -s $(expr $SLURM_ARRAY_TASK_ID / 2) -m $(expr $SLURM_ARRAY_TASK_ID % 2)
```

SLURM accepts a few flags (here in comments) that set some parameters.

* job-name allows you to distinguish this job from another in squeue
* nodes defines the number of machines required for this job
* ntasks is typically one for these scenarios
* cpus-per-task is how many CPU cores will be allocated for this task. If you run multicore programs, please set this parameter according to how many threads you will use (most software defines all CPUs available in the machine by default.)
* mem defines the required amount of memory. if you define the total memory in the machine, this will make each job sequencial.
* time defines a timeout for the job to run. The cluster will probably also have a global timeout (typically 24 or 48h).
* output defines where the stdout will be redirected. Since you do not have access to the machine that will run this, you need to read it later, after the job finishes. If you want (fake) synchronous execution, look for the `srun` command.
* gres defines how many GPUs will be allocated for this job. Note that if you do not define this, your software will have access to the GPU and can use it. It means that your program will run at the same time as others (who carefully set this parameter) and crash both yours and theirs programs. Please set this flag everytime GPUs are used! It is very important.
* array sets how many tasks you want (inclusive on both ends). 0-59 will crease 60 jobs. Since in this example we want to best two alternative models (A and B) each 30 times, we define that we want 60 parallel executions, and then we use the $SLURM_ARRAY_TASK_ID variable to obtain the 0-29 and the 0-1 values to pass as parameters.


# Other tips

* If you want to run long experiments, implement a snashot mechanism that saves backups of the results, in the case the machine crashes. Also implement a restore functionality so that you can submit a 3-month job as 24h smaller jobs that continue from the previous results. This way, other people can still use the cluster between your smaller jobs. Do not be an hoarder of resources.
* UV is a great tool for running different python versions with weird dependencies.