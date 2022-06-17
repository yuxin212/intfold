FROM scratch

SHELL ["/bin/bash", "-c"]

# Download Original AlphaFold
RUN rm -rf /app/intfold \
    && git clone https://github.com/deepmind/alphafold.git /app/intfold
RUN (cd /app/intfold; git checkout 1d43aaff941c84dc56311076b58795797e49107b --quiet)

# ColabFold patches
WORKDIR /app/intfold
RUN wget -qnc https://raw.githubusercontent.com/sokrypton/ColabFold/main/beta/colabfold.py \
    && wget -qnc https://raw.githubusercontent.com/sokrypton/ColabFold/main/beta/colabfold_alphafold.py \
    && wget -qnc https://raw.githubusercontent.com/sokrypton/ColabFold/main/beta/pairmsa.py \
    && wget -qnc https://raw.githubusercontent.com/sokrypton/ColabFold/main/beta/protein.patch \
    && wget -qnc https://raw.githubusercontent.com/sokrypton/ColabFold/main/beta/config.patch \
    && wget -qnc https://raw.githubusercontent.com/sokrypton/ColabFold/main/beta/model.patch \
    && wget -qnc https://raw.githubusercontent.com/sokrypton/ColabFold/main/beta/modules.patch \
    && wget -qnc https://raw.githubusercontent.com/YoshitakaMo/localcolabfold/main/gpurelaxation.patch -O gpurelaxation.patch 

# HH-suite
RUN wget -qnc https://raw.githubusercontent.com/soedinglab/hh-suite/master/scripts/reformat.pl

# Apply patches from Lim Heo @huhlim
RUN patch -u alphafold/common/protein.py -i protein.patch \
    && patch -u alphafold/model/model.py -i model.patch \
    && patch -u alphafold/model/modules.py -i modules.patch \
    && patch -u alphafold/model/config.py -i config.patch 

# Download AlphaFold Parameter
RUN mkdir -p /app/intfold/alphafold/data/params \
    && curl -fL "https://storage.googleapis.com/alphafold/alphafold_params_2021-07-14.tar" | tar -x -C /app/intfold/alphafold/data/params

# Download stereo_chemical_props.txt
WORKDIR /app/intfold/alphafold/common
RUN wget -q https://git.scicore.unibas.ch/schwede/openstructure/-/raw/7102c63615b64735c4941278d92b554ec94415f8/modules/mol/alg/src/stereo_chemical_props.txt

# Install Miniconda
RUN wget -q -P /tmp \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda \
    && rm /tmp/Miniconda3-latest-Linux-x86_64.sh

# Create conda environment and install packages
ENV PATH="/opt/conda/bin:$PATH"
RUN conda create -n intfold python=3.7 -y \
    && conda activate intfold \
    && conda update -y conda \
    && conda install -c conda-forge python=3.7 cudnn==8.2.1.32 cudatoolkit==11.1.1 openmm==7.5.1 pdbfixer pandas -y \
    && conda install -c bioconda hmmer==3.3.2 hhsuite==3.3.0 -y \
    && python3.7 -m pip install absl-py==0.13.0 biopython==1.79 chex==0.0.7 dm-haiku==0.0.4 dm-tree==0.1.6 immutabledict==2.0.0 jax==0.2.14 ml-collections==0.1.0 numpy==1.19.5 scipy==1.7.0 tensorflow-gpu==2.5.0 \
    && python3.7 -m pip install jupyter matplotlib py3Dmol tqdm \
    && python3.7 -m pip install --upgrade jax jaxlib==0.1.69+cuda111 -f https://storage.googleapis.com/jax-releases/jax_releases.html

# Apply OpenMM patch.
WORKDIR /opt/conda/envs/intfold/lib/python3.7/site-packages
RUN patch -p0 < /app/intfold/docker/openmm.patch

# Enable GPU-accelerated relaxation.
WORKDIR /app/intfold
RUN patch -u alphafold/relax/gpurelaxation.py -i gpurelaxation.patch

# Prepare input data
RUN cat uniprot-filtered-reviewed_yes.tab.gz.parta* > uniprot-filtered-reviewed_yes.tab.gz
RUN rm uniprot-filtered-reviewed_yes.tab.gz.parta*

# Finish installing and configuring 

# Running from here
WORKDIR /app/intfold
RUN echo $'#!/bin/bash\n \ 
    ldconfig\n \
    python /app/intfold/batch_intfold.py "$@"' > /app/run_intfold.sh \
    && chmod +x /app/run_intfold.sh

ENTRYPOINT ["/app/run_intfold.sh"]