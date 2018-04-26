import os

def Generate_feature_vector(fea_set, fin, fout):
	fea_vec_temp = []
	length_fea_set = len(fea_set)
	for i in range(length_fea_set):
		fea_vec_temp.append('0')

	classification = 1
	while True:
		for i in range(length_fea_set):
			fea_vec_temp[i] = '0'
		line = fin.readline()
		if line:
			if '-------------------' in line:
				classification = 0
			else:
				#print classification
				temp = line.split()
				if temp:
					for word in temp:
						if word in fea_set:
							fea_vec_temp[fea_set.index(word)] = '1'
				else:
					fea_vec_temp[fea_set.index('NULL')] = '1'
					#print 'bingo'

				fea_vec = ' '.join(fea_vec_temp) + '\n'
				#fea_vec = fea_vec + ' ' +str(classification) + '\n'
				fout.write(fea_vec)
		else:
			break


def Construct_feature_vector(path_fea_term_set, path_mid_uni_sin, path_mid_uni_mul):
	print '---------------------------'
	print 'start constructing feature vectors...'


	fin_fea_term_set = open(path_fea_term_set, 'r')
	fin_mid_uni_sin = open(path_mid_uni_sin, 'r')
	fin_mid_uni_mul = open(path_mid_uni_mul, 'r')
	
	fea_vec_filename = os.path.split(path_mid_uni_sin)[1].split('_')
	fea_vec_filename[0] = 'Feature_vector'
	fea_vec_filename = '_'.join(fea_vec_filename)
	fout_fea_vec_sin = open(os.path.split(path_mid_uni_sin)[0] + '/' + fea_vec_filename, 'w+')
	
	fea_vec_filename = os.path.split(path_mid_uni_mul)[1].split('_')
	fea_vec_filename[0] = 'Feature_vector'
	fea_vec_filename = '_'.join(fea_vec_filename)
	fout_fea_vec_mul = open(os.path.split(path_mid_uni_mul)[0] + '/' + fea_vec_filename, 'w+')


	fea_term_set = []
	line = fin_fea_term_set.readline() 
	line = fin_fea_term_set.readline()
	while True:
		line = fin_fea_term_set.readline()
		if line:
			fea_term_set.append(line.split()[0])
		else:
			break
	fin_fea_term_set.close()

	Generate_feature_vector(fea_term_set, fin_mid_uni_sin, fout_fea_vec_sin)
	Generate_feature_vector(fea_term_set, fin_mid_uni_mul, fout_fea_vec_mul)

	fin_mid_uni_sin.close()
	fin_mid_uni_mul.close()
	fout_fea_vec_sin.close()
	fout_fea_vec_mul.close()

if __name__ == '__main__':
	print 'debugging...' 
	os.listdir('..')
	Construct_feature_vector('../../Data/VSM_results/Middle_unigram/0/Feature_term_set.txt', '../../Data/VSM_results/Middle_unigram/0/Sequence_Middle_unigram_0.txt', '../../Data/VSM_results/Middle_unigram/0/Sequence_Middle_unigram_0-5.txt')
