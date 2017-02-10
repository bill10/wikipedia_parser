import utils
import os
import wikiparser
import time
from argparse import ArgumentParser

def build_parser():
	parser = ArgumentParser()
	parser.add_argument('--dir',type=str,
				dest='dir',
				help='directory to save the files',
				required=True)
	parser.add_argument('--namespace',type=int,
				dest='namespace',
				help='namespace to parser',
				required=True)
	parser.add_argument('--titlesdir',type=str,
				dest='titlesdir',
				help='directories to required titles')
	parser.add_argument('--download',action='store_true',
				dest='download',
				help='download or not')
	parser.add_argument('--f',type=str,
				dest='file_dir',
				help='directory to the file if dont download')
	parser.add_argument('--idx',type=int,
				dest='idx',
				help='index of files to parser',
				required=True)
	return parser

def main():
	parser = build_parser()
	args = parser.parse_args()

	if(args.titlesdir != None):
		with open(args.titlesdir) as f:
			titles_ = f.readlines()
			titles = set(titles_)

	else: titles = None
	if(args.download == True):
		LINKS = utils.parse_links()
		link = LINKS[args.idx]
		[logfile_dir, file_dir] = utils.download(link,args.idx,args.dir,args.dir,bg=False)
		unzipped_dir = utils.unzip(args.idx,file_dir,args.dir)
	else:
		assert os.path.exists(args.file_dir)
		unzipped_dir = args.file_dir

	wikiparser.parser(unzipped_dir,args.dir,args.idx,args.namespace,titles)

		
	
if __name__ == '__main__':
	main()
