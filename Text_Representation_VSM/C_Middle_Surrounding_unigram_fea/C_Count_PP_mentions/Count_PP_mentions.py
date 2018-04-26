import os

def Count(fin, fout):
	num = 0
	num_all = 0
	tag = 0				#used for contradiction between *** and ---------
	#for i in range(10):
	while True:
		line = fin.readline()
		if line:
			if '***' in line:
				if num_all != 0 and tag != 1:
					fout.write(str(num) + '\n')
				tag = 0
				fout.write(line)
				num = 0
			elif '-----------------' in line:
				fout.write(str(num) + '\n')
				fout.write(line)
				tag = 1
			else:
				num += 1
				num_all += 1
		else:
			fout.write(str(num) + '\n')
			break
	print num_all	

def Count_PP_mentions(path_sin, path_mul, lower_path_VSM):
	print '---------------------------'
	print 'start counting number of mentions corresponding to each protein pair...'

	fin_sin = open(path_sin, 'r')
	fin_mul = open(path_mul, 'r')

	if os.path.split(os.path.split(os.path.split(os.path.split(lower_path_VSM)[0])[0])[0])[1] != '':
		path_count_sin = lower_path_VSM+'/'+'Count_'+os.path.split(os.path.split(os.path.split(os.path.split(lower_path_VSM)[0])[0])[0])[1]+'_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_sin)[1].split('_',1)[1]
		path_count_mul = lower_path_VSM+'/'+'Count_'+os.path.split(os.path.split(os.path.split(os.path.split(lower_path_VSM)[0])[0])[0])[1]+'_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_mul)[1].split('_',1)[1]
	else:
		path_count_sin = lower_path_VSM+'/'+'Count_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_sin)[1].split('_',1)[1]
		path_count_mul = lower_path_VSM+'/'+'Count_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_mul)[1].split('_',1)[1]
		
	fout_count_sin = open(path_count_sin, 'w+')
	fout_count_mul = open(path_count_mul, 'w+')

	Count(fin_sin, fout_count_sin)
	Count(fin_mul, fout_count_mul)

	fin_sin.close()
	fin_mul.close()
	fout_count_sin.close()
	fout_count_mul.close()

	#return lower_path_VSM+'/'+'Count_'+os.path.split(path_sin)[1], lower_path_VSM+'/'+'Count_'+os.path.split(path_mul)[1]

if __name__ == '__main__':
	print 'debugging...' 
	path_sin = '../../Data/Preprocess_results/Middle_unigram/0/Middle_unigram_0.txt' 	
	path_mul = '../../Data/Preprocess_results/Middle_unigram/0/Middle_unigram_0-5.txt'
	lower_path_VSM = '../../Data/VSM_results/Middle_unigram/0'
	path1, path2 = Count_PP_mentions(path_sin, path_mul, lower_path_VSM)
	fin1 = open(path1, 'r')
	fin2 = open(path2, 'r')
	n = 0
	while True:
		line = fin1.readline()
		if line:
			if '***' not in line and '------------' not in line:
				n += int(line.split()[0])
		else:
			break
	print n
				
	fin1.close()
	fin2.close()

	
