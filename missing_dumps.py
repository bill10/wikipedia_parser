import glob

dumps=set()

with open('all_dumps.txt') as infile:
    for l in infile:
        dumps.add(l.strip())

files=glob.glob('*.tsv')
for f in files:
    dumps.discard(f[:-4])

with open('all_dumps.txt','w') as outfile:
    for f in dumps:
        outfile.write(f+'\n')

print(len(dumps))
