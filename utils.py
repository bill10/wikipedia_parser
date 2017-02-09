from urllib import request
from bs4 import BeautifulSoup
import re
import subprocess
import os

def parse_links():
	url = 'https://dumps.wikimedia.org/enwiki/20161201/'
	keyword = 'enwiki-20161201-pages-meta-history'
	file_format = 'bz2' 

	html = request.urlopen(url)
	soup = BeautifulSoup(html)
	raw_links = soup.find_all('a', string=re.compile(keyword))
	links = [os.path.join(url,link.text) 
			for link in raw_links if file_format in link.text]
	validify_links(url,links)

	return links

def download(link,idx,log_dir,down_dir):
	'''
	Download the links

	Args:
	=====
	link:		the link to be downloaded
	idx: 		the index
	log_dir:	the directory for saving the log files from wget
	down_dir:	the directory for saving the downloaded files

	Returns:
	========
	logfile_dir: 	the directory to the logged file 
	file_dir:	the directory to the downloaded file
	'''
	

	assert os.path.exists(log_dir)
	assert os.path.exists(down_dir)
	
	logfile_dir = os.path.join(log_dir,'log_wiki_history_%d'%(idx))
	file_dir = os.path.join(down_dir,'wiki_history_%d.xml.bz2'%(idx))	

	assert os.path.exists(logfile_dir) == False
	assert os.path.exists(file_dir) == False

	print('Download   Status: %d BEGIN'%(idx))

	subprocess.call('sudo wget -a %s -O %s -b %s'%
				(logfile_dir,file_dir,link),shell=True)

	return [logfile_dir, file_dir]


def unzip(idx,file_dir,unzip_dir):
	'''
	Unzip the file

	Args:
	=====
	idx: 		index
	file_dir: 	directory to the file to be unzipped
	unzip_dir:	directory for saving the unzipped file
	'''
	assert os.path.exists(file_dir)
	assert os.path.exists(unzip_dir)
	
	unzipped_dir = os.path.join(unzip_dir,'wiki_history_%d.xml'%(idx))
	assert os.path.exists(unzipped_dir) == False

	print('Decompress Status: %d BEGIN'%(idx))
	subprocess.call('sudo pv %s | sudo bzip2 -d > %s'
		%(file_dir, unzipped_dir),shell=True)
	print('Decompress Status: %d COMPLETE'%(idx))
	
	# delete the raw file after decompression to save space
	subprocess.call('sudo rm %s'%(file_dir),shell=True)
	assert os.path.exists(file_dir) == False
	print('Delete    Statis: %d COMPLETE)'%(idx)) 

def validify_links(url,links):
	link_example1 = 'enwiki-20161201-pages-meta-history7.xml-p000892914p000924158.bz2'
	link_example2 = 'enwiki-20161201-pages-meta-history26.xml-p041891164p042663461.bz2'
	link_example3 = 'enwiki-20161201-pages-meta-history11.xml-p003046514p003201200.bz2'
	assert( os.path.join(url,link_example1) in links and
		os.path.join(url,link_example2) in links and
		os.path.join(url,link_example3) in links)
	print('Validify Links: PASSESED')


def get_wget_progress(idx,logfile_dir):
	''' 
	Get the percentage progress of downloading

	Args:
	======
	idx: 		the index of the file to be downloaded
	logfile_dir:	the directory to the log file

	Return:
	========
	progress

	'''
	with open(logfile_dir) as f:
		txt_progress = f.readlines() # read the texts in the log file
		progress = [re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*",t) for  t in txt_progress[8:]]
			# filter all the numbers in the texts 
			# progress = [ bytes_downloaded, progress%, 
			#	       speed, minutes_remain, sec_remain]
	if(len(txt_progress) < 8): 
		# the first 8 lines of the log file contains only system info
		progress_to_return = 0
	
	elif (len(progress) < 10): 
		# the last ten lines are usually not complete
		progress_to_return = 0
	
	elif(txt_progress[-2].find('saved') > 0):
        	# this is when the download is complete
	        progress_to_return = 100

	else:
		progress_to_return = int(progress[-10][1])
	
	return progress_to_return
