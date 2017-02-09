import mwxml
import pandas as pd
import numpy as np
from argparse import ArgumentParser
from datetime import datetime as time

def build_parser():
	parser = ArgumentParser()
	parser.add_argument('--file', type=str,
                                dest = 'file_name',
                                help = 'dump file to parse',
                                metavar = 'FILE_NAME',
                                required = True)
	parser.add_argument('--limit', type=int,
                                dest = 'limit',
                                help = 'the number of queries to compute',
                                metavar = 'LIMIT',
                                required = True)
	parser.add_argument('--limit2print', type=int,
				dest = 'limit2print', 
				help = 'iteration idx to print', 
				metavar = 'LIMIT_2_PRINT', 
				required = False, default = None)
	parser.add_argument('--namespace', type=int,
				dest = 'namespace', 
				help = 'namespace to search',
				metavar = 'NAMESPACE', 
				required = False)
	parser.add_argument('--title', type=str,
				dest = 'title', 
				help  = 'title to search', 
				metavar = 'TITLE', 
				required = False)
	return parser



parser = build_parser()
args = parser.parse_args()

columns = ['Title','time','user','page','byte','comment']
df = pd.DataFrame(columns = columns)
idx = 0
time_start = time.now()

dump = mwxml.Dump.from_file(args.file_name)
for pages in dump: 
	if(pages.namespace == args.namespace):
		title = pages.title
		for revisions in pages._Page__revisions:
			if(revisions.text!=None):
				byte = len(revisions.text)
			else:
				byte = 0
			comment = revisions.comment
			page = revisions.page
			timestamp = revisions.timestamp
			user = revisions.user.text

			row  = pd.DataFrame([[title,timestamp,user,page,byte,comment]],columns=columns)
			df = df.append(row)

	if(idx >= args.limit): break
	if( (args.limit2print != None)  & (idx % args.limit2print == 0)): 
		print('iterations number %d, time elapsed = %s' % (idx, (time.now() - time_start)))
	
	idx = idx + 1


time_stop = time.now()
print('Time elapsed = %s' % (time_stop - time_start))
df.to_csv('output.csv')

