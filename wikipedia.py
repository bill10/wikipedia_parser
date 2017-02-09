import utils
import subprocess
import os
import wiki_parser
import time
from argparse import ArgumentParser

def build_parser():
	parser = ArgumentParser()
	parser.add_argument('--dir',type=str,
				dest='dir',
				help='directory',
				required=True)
	parser.add_argument('--limit', type=int,
				dest='limit',
				help='limit processing num',
				default=None)
	parser.add_argument('--limitfile', type=int,
				dest='limitfile',
				help='limit num of entries per file (for test)',
				default=None)
	parser.add_argument('--limit2print',type=int,
				dest='limit2print',
				help='print progress (for test)')
	parser.add_argument('--namespace',type=int,
				dest='namespace',
				help='namespaces to parse',
				required=True)
	parser.add_argument('--titlesdir',type=str,
				dest='titlesdir',
				help='directory to required titles',
				required=True)
	parser.add_argument('--download',type=bool,
				dest='download',
				help='whether to down the files',
				required=True)
	parser.add_argument('--filename',type=str,
				dest='filename',
				help='filename (for test)')
	return parser


def main():
	parser = build_parser()
	args = parser.parse_args()
	
	# hash the titles required 
	assert os.path.exists(args.titlesdir) 
	with open(args.titlesdir) as f:
		titles_ = f.readlines()
	titles = set(titles_)


	if(args.download == True):
		idx = 0
		[output_dir,log_dir,down_dir,unzip_dir] = make_directories(args.dir)
		file_dirs = download_and_unzip(args,log_dir,down_dir,unzip_dir)
	else: # for test only
		file_dirs = [args.filename]
	
	idx = 0
	for file_dir in file_dirs:
		wiki_parser.parser(file_dir,output_dir,idx,args.namespace,
			titles,args.limitfile,args.limit2print)
		print('File Parse: %d COMPLETE'%(idx))
		idx = idx + 1

def make_directories(dir):
	'''
	Make directories

	Return:
	=======
	[output_dir,
	logfile_dir,
	downloads_dir,
	unzipped_dir]
	'''

	assert os.path.exists(dir)

	output_dir = os.path.join(dir,'outputs')
	log_dir = os.path.join(dir,'logs')
	down_dir = os.path.join(dir,'downloads')
	unzip_dir = os.path.join(dir,'unzipped')
	
	dirs = [output_dir,log_dir,down_dir,unzip_dir]	
	for d in dirs:
		# 1. create directories
		# 2. give the system permission to read,write,execute
		subprocess.call('sudo mkdir %s'%(d),shell=True)
		subprocess.call('sudo chmod 777 %s'%(d),shell=True)
	
	print('Directories Created.')

	return dirs


def download_and_unzip(args,log_dir,down_dir,unzip_dir):
	
	LINKS = utils.parse_links()
	file_dirs = []

	for idx in range(len(LINKS)) if args.limit is None else range(args.limit):
		link = LINKS[idx]
		[logfile_dir, file_dir] = utils.download(link,idx,log_dir,down_dir)
		file_dirs.append(file_dir) # file_dirs = [file_dir[0] ... file_dir[n]]
		if(idx >= 1): # there are files to be decompressed
			assert os.path.exists(file_dirs[idx-1])
			utils.unzip(idx-1,file_dirs[idx-1],unzip_dir) 
		
		# after finishing decompression
		# wait until the current download is complete
		progress = utils.get_wget_progress(idx,logfile_dir)
		print('Download   Statis: %d WAITING'%(idx))
		gap = 5 # how often to print download progress
		while(progress<100):
			new_progress = utils.get_wget_progress(idx,logfile_dir)
			if(new_progress > progress+gap or new_progress == 100):
				print('\t Current Download Progress: ',new_progress,'%')
				progress = new_progress
			time.sleep(5) # reduce unnecessary accesses to log files
		print('Download   Statis: %d COMPLETE'%(idx))

	# decompress the last file (not included in the for loop)
	if(idx >= 1):
		assert os.path.exists(file_dirs[idx])
		utils.unzip(idx,file_dirs[idx],unzip_dir)
	
	print('ALL %d FILES ARE DECOMPRESSED / DOWNLOADED'%(len(LINKS)))
	
	return file_dirs		






if __name__ == '__main__':
	main()
