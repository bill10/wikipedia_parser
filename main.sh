#!/bin/bash
# This is to be run on every working node
module load gcc
module load stashcp

# Install miniconda3
bash Miniconda3-latest-Linux-x86_64.sh -b -p "${PWD}/miniconda3"

# Activate virtual environment
miniconda3/bin/conda create -y -n myenv python
source miniconda3/bin/activate myenv

# Install python packages
pip install mwxml.tar.gz
conda install -y pandas

tar -xf p7zip.tar.gz
stashcp /user/bill10/public/Wiki/$1 .
p7zip/bin/7z e $1

# Run python script
python wikipedia_osg.py $1

# deactivate virtual environment
source deactivate myenv

exit
