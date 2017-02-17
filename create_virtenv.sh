#!/bin/bash
# This is to be run on the login node
 
# Load python 2.7
module load python/2.7

# Activate virtual environment
virtualenv-2.7 virtenv
source virtenv/bin/activate

# Install python packages (some are unused in this demo)
pip install mwxml
pip install pandas

# Deactivate virtual environment
deactivate

# Compress virtual environment
tar -cvzf virtenv.tar.gz virtenv

rm -R virtenv

mkdir Log
