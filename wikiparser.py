import os
import mwxml
import pandas as pd
import numpy as np
import subprocess
from datetime import datetime as time

def parser(file_dir,output_dir,idx, 
			namespace,page_titles,limit=None,limit2print=10000):
	'''
	parse the wikipedia.xml file into csv

	Args:
	=====
	file_dir:	directory of the file to parse
	output_dir:	directory to the output.csv
	idx:		index
	namespace:	namespace to search 
	page_title: 	(set) titles of required pages

	limit: 		maximum number of entries per file (for test only)
	limit2print:	the frequency to print progress

	Return:
	=======
	outputfile_dir 	directory to the output file
	'''

	assert os.path.exists(file_dir)
	assert os.path.exists(output_dir)
	outputfile_dir = os.path.join(output_dir,'wiki_history_parsed_%d.csv'%(idx)) 
	subprocess.call('sudo chmod 777 %s'%(output_dir),shell=True)	

	columns = ['Title','time','user','byte']
	df = pd.DataFrame(columns = columns)
	i = 0
	time_start = time.now()

	dump = mwxml.Dump.from_file(file_dir)
	for pages in dump:
		if(pages.namespace == namespace):
			if(page_titles != None and 
				pages.title.replace(' ','').lower() not in page_titles):
				continue

			title = pages.title
			for revisions in pages._Page__revisions:
				if(revisions.text!=None):
					byte = len(revisions.text)
				else:
 					byte = 0
				timestamp = revisions.timestamp
				if (revisions.user != None):
					user = revisions.user.text
				else:
					user = 'NA'
				row  = pd.DataFrame([[title,timestamp,user,byte]],columns=columns)
				df = df.append(row)
		if( limit != None and i >= limit ): break
		if( (limit2print != None)  & (i % limit2print == 0)):
			print('iterations number %d, time elapsed = %s'%
				(i, (time.now() - time_start)))

		i = i + 1


	time_stop = time.now()
	print('Time elapsed = %s' % (time_stop - time_start))
	df.to_csv(outputfile_dir)
	
	return outputfile_dir
