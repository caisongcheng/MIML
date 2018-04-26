import os

from A_Extract_feature_term import Extract_feature_term
from B_Construct_feature_vector import Construct_feature_vector
from C_Count_PP_mentions import Count_PP_mentions

def Middle_Surrounding_unigram_fea(upper_path_pre, upper_path_VSM):									#incoming parameter is the path of preprocess result and the path of VSM result
	print '\n*********************************************************************\n'
	print 'start constructing feature vectors using middle & surrounding unigram as feature term...\n'

	print upper_path_pre
	print upper_path_VSM
	for direct1 in sorted(os.listdir(upper_path_pre)):
		if not os.path.exists(upper_path_VSM+'/'+direct1):									
			os.makedirs(upper_path_VSM+'/'+direct1) 											#make corresponding directory for VSM, here, e.g. 1/ 2/, etc.

		path_sin = upper_path_pre+'/'+direct1 + '/' + sorted(filter(lambda x: os.path.isfile(upper_path_pre+'/'+direct1+'/'+x), os.listdir(upper_path_pre+'/'+direct1)))[1]
		path_mul = upper_path_pre+'/'+direct1 + '/' + sorted(filter(lambda x: os.path.isfile(upper_path_pre+'/'+direct1+'/'+x), os.listdir(upper_path_pre+'/'+direct1)))[0]

		path_fea_term_set, path_mid_sur_uni_sin, path_mid_sur_uni_mul = Extract_feature_term.Extract_feature_term(path_sin, path_mul, upper_path_VSM+'/'+direct1)
																								#call the Extract_feature_term model to extract the feature terms first, incoming parameters are path of input file including single part and multiple parts of preprocess result and the path to save the VSM results

		Construct_feature_vector.Construct_feature_vector(path_fea_term_set, path_mid_sur_uni_sin, path_mid_sur_uni_mul)

		Count_PP_mentions.Count_PP_mentions(path_sin, path_mul, upper_path_VSM+'/'+direct1)

		for direct2 in filter(lambda x: os.path.isdir(upper_path_pre+'/'+direct1+'/'+x), os.listdir(upper_path_pre+'/'+direct1)):
			if not os.path.exists(upper_path_VSM+'/'+direct1+'/'+direct2):
				os.mkdir(upper_path_VSM+'/'+direct1+'/'+direct2)
			for direct3 in sorted(os.listdir(upper_path_pre+'/'+direct1+'/'+direct2)):
				if not os.path.exists(upper_path_VSM+'/'+direct1+'/'+direct2+'/'+direct3):
					os.mkdir(upper_path_VSM+'/'+direct1+'/'+direct2+'/'+direct3)
				
				lower_path_VSM = upper_path_VSM+'/'+direct1+'/'+direct2+'/'+direct3

				path_sin_tra = upper_path_pre+'/'+direct1+'/'+direct2+'/'+direct3+'/'+os.listdir(upper_path_pre+'/'+direct1+'/'+direct2+'/'+direct3)[1]
				path_mul_tra = upper_path_pre+'/'+direct1+'/'+direct2+'/'+direct3+'/'+os.listdir(upper_path_pre+'/'+direct1+'/'+direct2+'/'+direct3)[0]
				
				path_fea_term_set_tra, path_mid_sur_uni_sin_tra, path_mid_sur_uni_mul_tra = Extract_feature_term.Extract_feature_term(path_sin_tra, path_mul_tra, lower_path_VSM)

				Construct_feature_vector.Construct_feature_vector(path_fea_term_set, path_mid_sur_uni_sin_tra, path_mid_sur_uni_mul_tra)

				Count_PP_mentions.Count_PP_mentions(path_sin_tra, path_mul_tra, lower_path_VSM)



if __name__ == '__main__':
	print 'debugging...' 
	os.chdir('../../Data')
	path_sin = 'Preprocess/Merge results/unigram/0/unigram_0.txt' 	
	path_mul = 'Preprocess/Merge results/unigram/0/unigram_0-5.txt'
	lower_path_VSM = 'VSM/Surrounding_unigram/0'
	Extract_feature_term.Extract_feature_term(path_sin, path_mul, lower_path_VSM)
