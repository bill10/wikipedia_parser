import os
import sys
import subprocess
import mwxml
import pandas as pd
import time

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
    infile:	the file to parse
    outfile: 	filename of the output file
    namespace:	namespace to search
    page_title: 	(set) titles of required pages
    '''

    i = 0
    dump = mwxml.Dump.from_file(infile)
    title=[]
    byte=[]
    user=[]
    timestamp=[]
    for pages in dump:
        if(pages.namespace == namespace):
            if(page_titles != None and pages.title.replace(' ','').lower() not in page_titles):
                continue
            prev=0
            for revisions in pages:
                title.append(pages.title)
                if(revisions.text!=None):
                    byte.append(len(revisions.text)-prev)
                    prev=len(revisions.text)
                else:
                    byte.append(0)
                timestamp.append(revisions.timestamp)
                if (revisions.user != None):
                    user.append(revisions.user.text)
                else:
                    user.append('')
        if( limit != None and i >= limit ):
            break
        i = i + 1
    df  = pd.DataFrame({'title':title,'time':timestamp,'user':user,'byte':byte})
    df.to_csv(outfile, sep='\t', index=False)


def main():
    namespace=1
    titles=None
    with open('page_titles.txt') as f:
    	titles_ = f.readlines()
    	titles = set(titles_)
    base_url = 'https://dumps.wikimedia.org/enwiki/20161201/'
    filename=sys.argv[1]
    url = base_url+filename
    tic.go('Downloading {}...'.format(filename))
    subprocess.call(["wget", url])
    tic.stop()
    tic.go('Decompresing...')
    subprocess.call(["bzip2", "-d", filename])
    tic.stop()
    tic.go('Parsing...')
    infile=filename[:-4]
    outfile=filename+'.tsv'
    parser(infile,outfile,namespace,titles)
    tic.stop()
    #subprocess.call(["rm", filename])
    #subprocess.call(["rm", infile])

if __name__ == '__main__':
	main()
