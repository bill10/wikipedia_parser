#!/bin/bash
# This is to be run on every working node

# load necessary modules
module load python/2.7
module load lapack
module load gcc

# untar and activate virtual environment
tar -xzf virtenv.tar.gz
source ./virtenv/bin/activate

# Run python script
./virtenv/bin/python2.7 wikipedia_osg.py $1

# deactivate virtual environment
deactivate
