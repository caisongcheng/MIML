import re
import os

def Extract_feature_term(path_sin, path_mul, lower_path_VSM):								#incoming parameters are path of input file including single part and multiple parts of preprocess result and the path to save the VSM results
	print '---------------------------'
	print 'start extracting feature terms...'

	fin_sin = open(path_sin, 'r')															#path_sin is the relative path of single division part after preprocess and linguistic process, relative to the main py file
	fin_mul = open(path_mul, 'r')															#path_sin is the relative path of single division part after preprocess and linguistic process, relative to the main py file
	fout_fea_term_list = open(lower_path_VSM+'/'+'Feature_term_list.txt', 'w+')
	fout_fea_term_set = open(lower_path_VSM+'/'+'Feature_term_set.txt', 'w+')
	if os.path.split(os.path.split(os.path.split(os.path.split(lower_path_VSM)[0])[0])[0])[1] != '':
		path_mid_uni_sin = lower_path_VSM+'/'+'Sequence_'+os.path.split(os.path.split(os.path.split(os.path.split(lower_path_VSM)[0])[0])[0])[1]+'_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_sin)[1].split('_',1)[1]
		path_mid_uni_mul = lower_path_VSM+'/'+'Sequence_'+os.path.split(os.path.split(os.path.split(os.path.split(lower_path_VSM)[0])[0])[0])[1]+'_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_mul)[1].split('_',1)[1]
	else:
		path_mid_uni_sin = lower_path_VSM+'/'+'Sequence_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_sin)[1].split('_',1)[1]
		path_mid_uni_mul = lower_path_VSM+'/'+'Sequence_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_mul)[1].split('_',1)[1]
		
	fout_mid_uni_sin = open(path_mid_uni_sin, 'w+')
	fout_mid_uni_mul = open(path_mid_uni_mul, 'w+')
																							#make the file of feature term and feature list through multiple division parts and sequence of single and multiple division parts corresponding to the path of Preprocess_results 


	fea_term_list = []																		#list to store the feature term
	while True: 
		line = fin_mul.readline()															#all the operation below is for multiple divisin parts
		if line:
			matchOBJ = re.match(r'(.*)#(.*)#(.*)#(.*)#(.*)',line,re.I)						#if match that pattern, it means that this is a sentence corresponding to one protein pair 
			if matchOBJ:
				temp = matchOBJ.group(3).split()											#group(3) is the middle unigram between two protein pairs
				if not temp:
					temp = ['NULL']															#if there is nothing between two protein pairs, then set temp as NULL for 
				fea_term_list.extend(temp)													#add the feature term into a list, which might be repeated
				#print temp

				fout_mid_uni_mul.write(str(matchOBJ.group(3)) + '\n')						#write the the middle unigram between two protein pairs into file as the representation in the aspect of middle_unigram 
			elif '-------------' in line:
				fout_mid_uni_mul.write(line)												#write the dividing line into file, too
		else:
			break

	fea_term_set = set(fea_term_list)														#set of feature term is non-repeated
	print 'length of list of feature term:', len(fea_term_list)
	print 'length of set of feature term:', len(fea_term_set)

	fout_fea_term_list.write('count:'+str(len(fea_term_list)) + '\n\n')						#write the length of list into file first
	for term in fea_term_list:
		fout_fea_term_list.write(str(term) + '\n')											#write every term of the list into file

	fout_fea_term_set.write('count:'+str(len(fea_term_set)) + '\n\n')						#write the length of set into file first
	for term in fea_term_set:
		fout_fea_term_set.write(str(term) + '\n')											#write every term of the set into file

	while True:
		line = fin_sin.readline()															#this is for single division part, just to give the sequence of middle unigram for test
		if line:
			matchOBJ = re.match(r'(.*)#(.*)#(.*)#(.*)#(.*)',line,re.I)						#if match that pattern, it means that this is a sentence corresponding to one protein pair 
			if matchOBJ:
				fout_mid_uni_sin.write(str(matchOBJ.group(3)) + '\n')						#group(3) is the middle unigram between two protein pairs
			elif '-------------' in line:
				fout_mid_uni_sin.write(line)												#write the dividing line into file, too
		else:
			break

	fin_sin.close()
	fin_mul.close()
	fout_fea_term_list.close()
	fout_fea_term_set.close()
	fout_mid_uni_sin.close()
	fout_mid_uni_mul.close()

	path_fea_term_set = lower_path_VSM+'/'+'Feature_term_set.txt'							#path of the feature term set, for the construction of feature vector

	return path_fea_term_set, path_mid_uni_sin, path_mid_uni_mul							#return three paths for the next function

