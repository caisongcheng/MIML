import os
import shutil

def merge_parts(low_dir_ling, low_dir_mer):
	print 
	print '-----------------------------------------------------------'
	print 'start meiging parts of cross validation for testing...'

	'''for direct in low_dir_ling:
		print os.path.split(direct)
	
	for direct in low_dir_ling:
		for list_direct in os.listdir(direct):
			print os.path.splitext(list_direct)[0][-2:]

	for direct in low_dir_ling:
		print sorted(os.listdir(direct))'''

	num_div = len(os.listdir(low_dir_ling[0]))

	for i in range(num_div):
		for direct in low_dir_mer:
			if not os.path.exists(direct+'/'+str(i)):
				os.makedirs(direct+'/'+str(i))

	top_dir_mer = os.path.split(low_dir_mer[0])[0]

	for direct in low_dir_ling:
		for file_ling in sorted(os.listdir(direct)):

			fout = open(top_dir_mer+'/'+os.path.split(direct)[1]+'/'+os.path.splitext(file_ling)[0][-1]+'/'+os.path.splitext(file_ling)[0]+'-'+str(num_div)+'.txt', 'w+')

			for file_ling_oth in sorted(os.listdir(direct)):
				if file_ling != file_ling_oth:
					fin = open(direct+'/'+file_ling_oth, 'r')
					while True:
						line = fin.readline()
						if line:
							if '----------' not in line:
								#print line
								fout.write(line)
							else:
								break
					fin.close()

			fout.write('--------------------------------------dividing line for interactive and non-interactive protein pairs----------------------------------------------\n')

			for file_ling_oth in sorted(os.listdir(direct)):
				if file_ling != file_ling_oth:
					fin = open(direct+'/'+file_ling_oth, 'r')
					while True:
						line = fin.readline()
						if line:
							if '----------' in line:
								while True:
									line = fin.readline()
									if line:
										#print line
										fout.write(line)
									else:
										break
						if not line:
							break
					fin.close()

			fout.close()

			shutil.copyfile(direct+'/'+file_ling, top_dir_mer+'/'+os.path.split(direct)[1]+'/'+os.path.splitext(file_ling)[0][-1]+'/'+file_ling)
			
