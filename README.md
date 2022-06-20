# IntFold
Generating intermediate representations using AlphaFold2 and ColabFold

## Overview
This repo uses Evoformer of [AlphaFold2](https://github.com/deepmind/alphafold) to generate intermediate representations (MSA and Pair) for proteins, especially enzymes with EC numbers. The code is based on [ColabFold](https://github.com/sokrypton/ColabFold) and [LocalColabFold](https://github.com/YoshitakaMo/localcolabfold). 

The enzyme dataset is splitted in four files: 
`uniprot-filtered-reviewed_yes.tab.gz.partaa, uniprot-filtered-reviewed_yes.tab.gz.partab, uniprot-filtered-reviewed_yes.tab.gz.partac, uniprot-filtered-reviewed_yes.tab.gz.partad`,
comes from [UniProt](https://www.uniprot.org/). 

## Install
Only Linux is supported to run IntFold, please install Windows Subsystem for Linux if you are using Windows 10 or later. 

1. Install [Docker](https://www.docker.com/)
    - Install [nVidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) if you have nVidia GPUs
    - Set up [Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
    - Check if your nVidia Container Toolkit installation is successful by running
    
    ```
    docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
    ```
    Output lists your available GPUs, if no GPU is listed, check if you have followed the instruction of installing nVidia Container Toolkit and take a look at [nVidia docker issues](https://github.com/NVIDIA/nvidia-docker/issues)
    
2. If you don't need to modify the code, you can directly use [this built docker image](https://hub.docker.com/r/yuxin60/intfold) by running
    
    ```
    docker pull yuxin60/intfold
    ```
    
3. If you need to modify the code to run your tasks, first clone this repo and `cd` into it
    
    ```
    git clone https://github.com/yuxin212/intfold.git
    ```
    
    And modify the code accordingly. 
    
4. Build docker image

    ```
    docker build -f docker/Dockerfile -t intfold .
    ```
    
## Running IntFold

1. First run 

    ```
    docker run --gpus <number of gpus> yuxin60/intfold:latest
    ```
    
2. Get Container id
    
    ```
    docker ps
    ```

3. After running, copy generated intermediate representations from docker container to host

    ```
    docker cp <container-id>:/app/intermediate/ <path to store results>
    ```
    
4. After copying the output, please remove the docker container

    ```
    docker stop <container-id>
    docker rm <container-id>
    ```

### IntFold Output

The output will be saved as numpy arrays in docker container, and path is `/app/intermediate/`. This directory has the following structure:

```
/app/intermediate/<EC 1st number>/<EC 2nd number>/<EC 3rd number>/<EC 4th number>/
    <Entry>_msa_first_row.npy
    <Entry>_msa.npy
    <Entry>_pair.npy
    <Entry>_single.npy
```

Content of each output file, where `r` is number of amino acid residues:

`<Entry>_msa_first_row.npy`: First row of MSA representation, shape: `(512, r, 256)`

`<Entry>_msa.npy`: Full MSA representation, shape: `(r, 256)`

`<Entry>_pair.npy`: Pair representation, shape: `(r, r, 128)`

`<Entry>_single.npy`: Single Representation, shape: `(r, 384)`

## Citation

If you use this source code for your publication, plase cite 
1. Mirdita M, Schütze K, Moriwaki Y, Heo L, Ovchinnikov S and Steinegger M. ColabFold: Making protein folding accessible to all.
Nature Methods (2022) doi: [10.1038/s41592-022-01488-1](https://www.nature.com/articles/s41592-022-01488-1)

2. Jumper et al. "Highly accurate protein structure prediction with AlphaFold."
Nature (2021) doi: [10.1038/s41586-021-03819-2](https://doi.org/10.1038/s41586-021-03819-2)

3. If you use AlphaFold-multimer, please cite
Evans et al. "Protein complex prediction with AlphaFold-Multimer."
biorxiv (2021) doi: [10.1101/2021.10.04.463034v1](https://www.biorxiv.org/content/10.1101/2021.10.04.463034v1)
