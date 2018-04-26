import os

def Generate_feature_vector(fea_term_set_mid, fea_term_set_sur, fin_mid_uni, fin_sur_uni, fout):
	
	fea_vec_temp_mid = []
	length_fea_term_set_mid = len(fea_term_set_mid)
	for i in range(length_fea_term_set_mid):
		fea_vec_temp_mid.append('0')

	fea_vec_temp_sur = []
	length_fea_term_set_sur = len(fea_term_set_sur)
	for i in range(length_fea_term_set_sur):
		fea_vec_temp_sur.append('0')
	
	
	classification = 1
	while True:
		for i in range(length_fea_term_set_mid):
			fea_vec_temp_mid[i] = '0'
		for i in range(length_fea_term_set_sur):
			fea_vec_temp_sur[i] = '0'

		line_mid = fin_mid_uni.readline()
		line_sur = fin_sur_uni.readline()
		if line_mid and line_sur:
			if '-------------------' in line_mid and '-------------------' in line_sur:
				classification = 0
			else:
				#print classification
				temp_mid = line_mid.split()
				temp_sur = line_sur.split()
				if temp_mid:
					for word in temp_mid:
						if word in fea_term_set_mid:
							fea_vec_temp_mid[fea_term_set_mid.index(word)] = '1'
				else:
					fea_vec_temp_mid[fea_term_set_mid.index('NULL')] = '1'

				if temp_sur:
					for word in temp_sur:
						if word in fea_term_set_sur:
							fea_vec_temp_sur[fea_term_set_sur.index(word)] = '1'
				else:
					fea_vec_temp_sur[fea_term_set_sur.index('NULL')] = '1'
					#print 'bingo'

				fea_vec = ' '.join(fea_vec_temp_mid+fea_vec_temp_sur) + '\n'
				#fea_vec = fea_vec + ' ' +str(classification) + '\n'
				fout.write(fea_vec)
		else:
			break


def Construct_feature_vector(path_fea_term_set, path_mid_sur_uni_sin, path_mid_sur_uni_mul):
	print '---------------------------'
	print 'start constructing feature vectors...'


	fin_fea_term_set_mid = open(path_fea_term_set[0], 'r')
	fin_fea_term_set_sur = open(path_fea_term_set[1], 'r')
	fin_mid_uni_sin = open(path_mid_sur_uni_sin[0], 'r')
	fin_mid_uni_mul = open(path_mid_sur_uni_mul[0], 'r')
	fin_sur_uni_sin = open(path_mid_sur_uni_sin[1], 'r')
	fin_sur_uni_mul = open(path_mid_sur_uni_mul[1], 'r')
	
	fea_vec_filename_sin = os.path.split(path_mid_sur_uni_sin[0])[1].split('_')
	fea_vec_filename_sin[0] = 'Feature_vector'
	fea_vec_filename_sin[1] = 'middle_surrounding'
	fea_vec_filename_sin = '_'.join(fea_vec_filename_sin)
	fout_fea_vec_sin = open(os.path.split(path_mid_sur_uni_sin[0])[0] + '/' + fea_vec_filename_sin, 'w+')
	
	fea_vec_filename_mul = os.path.split(path_mid_sur_uni_mul[0])[1].split('_')
	fea_vec_filename_mul[0] = 'Feature_vector'
	fea_vec_filename_mul[1] = 'middle_surrounding'
	fea_vec_filename_mul = '_'.join(fea_vec_filename_mul)
	fout_fea_vec_mul = open(os.path.split(path_mid_sur_uni_mul[0])[0] + '/' + fea_vec_filename_mul, 'w+')

	print fea_vec_filename_sin
	print fea_vec_filename_mul

	fea_term_set_mid = []
	fea_term_set_sur = []
	line = fin_fea_term_set_mid.readline() 
	line = fin_fea_term_set_mid.readline()
	line = fin_fea_term_set_sur.readline() 
	line = fin_fea_term_set_sur.readline()
	while True:
		line1 = fin_fea_term_set_mid.readline()
		if line1:
			fea_term_set_mid.append(line1.split()[0])
		else:
			break
	while True:
		line2 = fin_fea_term_set_sur.readline()
		if line2:
			fea_term_set_sur.append(line2.split()[0])
		else:
			break
	fin_fea_term_set_mid.close()
	fin_fea_term_set_sur.close()

	Generate_feature_vector(fea_term_set_mid, fea_term_set_sur, fin_mid_uni_sin, fin_sur_uni_sin, fout_fea_vec_sin)
	Generate_feature_vector(fea_term_set_mid, fea_term_set_sur, fin_mid_uni_mul, fin_sur_uni_mul, fout_fea_vec_mul)

	fin_mid_uni_sin.close()
	fin_mid_uni_mul.close()
	fin_sur_uni_sin.close()
	fin_sur_uni_mul.close()

	fout_fea_vec_sin.close()
	fout_fea_vec_mul.close()

if __name__ == '__main__':
	print 'debugging...' 
	os.listdir('..')
	Construct_feature_vector('../../Data/VSM_results/Middle_unigram/0/Feature_term_set.txt', '../../Data/VSM_results/Middle_unigram/0/Sequence_Middle_unigram_0.txt', '../../Data/VSM_results/Middle_unigram/0/Sequence_Middle_unigram_0-5.txt')
