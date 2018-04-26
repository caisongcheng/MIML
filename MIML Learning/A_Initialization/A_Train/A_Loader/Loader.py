import numpy as np

def Loader(path_count_mul, path_fea_vec_mul):
	print 	
	print '-------------------------------------------------------------'
	print 'start loading feature vector and classifications...'
	print 

	X_ment = np.loadtxt(path_fea_vec_mul, dtype=int)		#matrix
	
	y_rela = []				#list
	y_ment = []				#list
	y_X = [[]]				#list
	y_X_num = []			#list
	i = -1
	classification = 1
	fin = open(path_count_mul, 'r')
	while True:
		line = fin.readline()
		if line:
			if '***' in line:
				i += 1
				if i != 0:
					y_X.append([])
				#y_X[i].append(line)
				y_rela.append(classification)
			elif '-------------' in line:
				classification = 0
			else:
				y_X_num.append(int(line))
				for j in range(int(line)):
					y_ment.append(classification)
					y_X[i].append(classification)
		else:
			break


	'''f_count_sen_num_csv.writerow(y_X_num)

	for i in range(len(y_X_num)):
		y_X_num[i] += 1
	f_count_sen_num_pp_csv.writerow(y_X_num)'''

	print X_ment.shape
	print len(y_ment)
	print len(y_X)
	print len(y_rela)

	return X_ment, y_rela, y_ment, y_X
