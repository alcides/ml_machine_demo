How to use the machine-learning machine @ DI-FCUL
=================================================


1. Setup your .ssh/config, based on ssh_config file

2. `scp -r gpu ml:` # to copy all these files to the server

3. `ssh ml` to enter the machine

4. `cd gpu && sbatch run.sh` to submit the job

5. `squeue` to see more info about the job