#!/bin/bash
#SBATCH --job-name=wikiparser
#SBATCH --output=%A_%a.out
#SBATCH --error=%A_%a.err
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=5:00:00
#SBATCH --mem=1000

# load python and packages
module add python
#export PYTHONPATH=/nas/longleaf/home/bill10/Library/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=/nas/longleaf/home/bill10/Library/lib/python3.5/site-packages:$PYTHONPATH

# Copy files from Stash
wget http://stash.osgconnect.net/+bill10/Wiki/enwiki-20161201-pages-meta-history13.xml-p005040438p005137507.7z
7z e enwiki-20161201-pages-meta-history13.xml-p005040438p005137507.7z 

# Run python script
python wikipedia_osg.py enwiki-20161201-pages-meta-history13.xml-p005040438p005137507.7z 
