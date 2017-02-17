#!/bin/bash
# This is to be run on every working node

# Install miniconda3
bash Miniconda3-latest-Linux-x86_64.sh -b -p "${PWD}/miniconda3"

# Activate virtual environment
miniconda3/bin/conda create -y -n myenv python
source miniconda3/bin/activate myenv

# Install python packages
conda install -y pip
pip install mwxml
conda install -y pandas

# Run python script
python wikipedia_osg.py $1

# deactivate virtual environment
source deactivate myenv
