import os
import sys
import subprocess
import mwxml
import pandas as pd
import time
from multiprocessing import Pool, cpu_count

class Stopwatch:
    start_time=None
    def go(self,msg=''):
        if msg:
            print(msg),
        self.start_time=time.time()
        sys.stdout.flush()
    def stop(self,msg=''):
        if msg:
            print("{}: {} seconds".format(msg,time.time()-self.start_time))
        else:
            print("Elapsed time: {} seconds".format(time.time()-self.start_time))
        sys.stdout.flush()
    def check(self):
        return time.time()-self.start_time

tic=Stopwatch()

def parser(infile,outfile,namespace,page_titles,limit=None):
    '''
    parse the wikipedia.xml file into csv

    Args:
    =====
    infile:    the file to parse
    outfile:     filename of the output file
    namespace:    namespace to search
    page_title:     (set) titles of required pages
    '''

    i = 0
    dump = mwxml.Dump.from_file(infile)
    title=[]
    byte=[]
    user=[]
    timestamp=[]
    for page in dump:
        if (page.namespace == namespace):
            if (len(page_titles)>0 and page.title.replace(' ','').lower() not in page_titles):
                continue
            prev=0
            for revision in page:
                title.append(page.title)
                if(revision.text!=None):
                    byte.append(len(revision.text)-prev)
                    prev=len(revision.text)
                else:
                    byte.append(0)
                timestamp.append(revision.timestamp)
                if (revision.user != None):
                    user.append(revision.user.text)
                else:
                    user.append('')
        if( limit != None and i >= limit ):
            break
        i = i + 1
    df  = pd.DataFrame({'title':title,'time':timestamp,'user':user,'byte':byte})
    df.to_csv(outfile, sep='\t', index=False)

def mapper(filename):
    namespace=1
    base_url = 'https://dumps.wikimedia.org/enwiki/20161201/'
    url = base_url+filename
    tic.go('Downloading {}...'.format(filename))
    subprocess.call(["wget", url])
    tic.stop()
    tic.go('Decompresing...')
    subprocess.call(["7z", "e", filename])
    tic.stop()
    tic.go('Parsing...')
    infile=filename[:-3]
    outfile=filename+'.tsv'
    parser(infile,outfile,namespace,titles)
    tic.stop()
    subprocess.call(["rm", filename])
    subprocess.call(["rm", infile])

if __name__ == '__main__':
    titles=set()
    with open('page_titles.txt') as f:
        for l in f:
            titles.add(l.strip('\n"'))
    dumps=[]
    with open('all_dumps.txt') as f:
        for l in f:
            dumps.append(l.strip('\n'))
    pool=Pool(cpu_count())
    pool.map(mapper,dumps)
    pool.join()
    pool.close()
