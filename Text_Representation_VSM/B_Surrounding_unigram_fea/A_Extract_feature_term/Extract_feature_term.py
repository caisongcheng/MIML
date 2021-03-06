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
		path_sur_uni_sin = lower_path_VSM+'/'+'Sequence_'+os.path.split(os.path.split(os.path.split(os.path.split(lower_path_VSM)[0])[0])[0])[1]+'_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_sin)[1].split('_',1)[1]
		path_sur_uni_mul = lower_path_VSM+'/'+'Sequence_'+os.path.split(os.path.split(os.path.split(os.path.split(lower_path_VSM)[0])[0])[0])[1]+'_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_mul)[1].split('_',1)[1]
	else:
		path_sur_uni_sin = lower_path_VSM+'/'+'Sequence_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_sin)[1].split('_',1)[1]
		path_sur_uni_mul = lower_path_VSM+'/'+'Sequence_'+os.path.split(os.path.split(lower_path_VSM)[0])[1]+'_'+os.path.split(path_mul)[1].split('_',1)[1]
		
	fout_sur_uni_sin = open(path_sur_uni_sin, 'w+')
	fout_sur_uni_mul = open(path_sur_uni_mul, 'w+')
																							#make the file of feature term and feature list through multiple division parts and sequence of single and multiple division parts corresponding to the path of Preprocess_results 


	num_sur = 2																				#number of words surrounds the two protein names	
	fea_term_list = []																		#list to store the feature term
	while True:
		line = fin_mul.readline()															#all the operation below is for multiple divisin parts
		if line:
			matchOBJ = re.match(r'(.*)#(.*)#(.*)#(.*)#(.*)',line,re.I)						#if match that pattern, it means that this is a sentence corresponding to one protein pair 
			if matchOBJ:
				temp1 = matchOBJ.group(1).split()											#group(1) is the left unigram of the first protein name
				temp2 = matchOBJ.group(5).split()											#group(5) is the right unigram of the second protein name
				temp = []																	#set temp as null every time deal with a new sentence

				if (len(temp1)-1) < num_sur:
					for i in range(len(temp1)-1):
						temp.append(temp1[-(len(temp1)-1-i)])
				else:
					for i in range(num_sur):
						temp.append(temp1[-(num_sur-i)])

				if len(temp2) < num_sur:
					for i in range(len(temp2)):
						temp.append(temp2[i])
				else:
					for i in range(num_sur):
						temp.append(temp2[i])

				'''if len(temp1) == 2:											
					temp.append(temp1[-1])													#if there are two words, the first is the number of sentence, so we just add the second word
				elif len(temp1) >= 3:	
					temp.append(temp1[-2])
					temp.append(temp1[-1])													#if there are words more than three, it means that except the first word ad the number of sentence, there are still at least two words on the left of the first protein name, so we add the last one and the las but not one words into temp
				if len(temp2) == 1:
					temp.append(temp2[0])													#if there is one word, we add the only word into temp, it is clear that if no word exists, we could add nothing
				elif len(temp2) >= 2:
					temp.append(temp2[0])
					temp.append(temp2[1])													#if there are two words, the first and the second word would be added into temp'''

				if not temp:
					temp = ['NULL']															#if there is nothing surrounds two protein names, then set temp as NULL
				fea_term_list.extend(temp)													#add the feature term into a list, which might be repeated
				#print temp

				if temp != ['NULL']:
					fout_sur_uni_mul.write(' '.join(temp) + '\n')							#if temp is not 'NULL', which means that there are words surrounds surrounds the two protein names, so use join to transfer temp from a list to a string that is split by space, and write into file
				else:
					fout_sur_uni_mul.write(' \n')											#if temp is 'NULL', which means that there is nothin surrounds the two protein names, so just write a space and a enter into file
			elif '-------------' in line:
				fout_sur_uni_mul.write(line)												#write the dividing line into file, too
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
				temp1 = matchOBJ.group(1).split()											#group(1) is the left unigram of the first protein name
				temp2 = matchOBJ.group(5).split()											#group(5) is the right unigram of the second protein name
				temp = []																	#set temp as null every time deal with a new sentence

				if (len(temp1)-1) < num_sur:
					for i in range(len(temp1)-1):
						temp.append(temp1[-(len(temp1)-1-i)])
				else:
					for i in range(num_sur):
						temp.append(temp1[-(num_sur-i)])		

				if len(temp2) < num_sur:
					for i in range(len(temp2)):
						temp.append(temp2[i])
				else:
					for i in range(num_sur):
						temp.append(temp2[i])
														
				'''if len(temp1) == 2:											
					temp.append(temp1[-1])													#if there are two words, the first is the number of sentence, so we just add the second word
				elif len(temp1) >= 3:	
					temp.append(temp1[-2])
					temp.append(temp1[-1])													#if there are words more than three, it means that except the first word ad the number of sentence, there are still at least two words on the left of the first protein name, so we add the last one and the las but not one words into temp
				if len(temp2) == 1:
					temp.append(temp2[0])													#if there is one word, we add the only word into temp, it is clear that if no word exists, we could add nothing
				elif len(temp2) >= 2:
					temp.append(temp2[0])
					temp.append(temp2[1])													#if there are two words, the first and the second word would be added into temp'''

				if not temp:
					temp = ['NULL']															#if there is nothing surrounds two protein names, then set temp as NULL

				#print temp

				if temp != ['NULL']:
					fout_sur_uni_sin.write(' '.join(temp) + '\n')							#if temp is not 'NULL', which means that there are words surrounds surrounds the two protein names, so use join to transfer temp from a list to a string that is split by space, and write into file
				else:
					fout_sur_uni_sin.write(' \n')											#if temp is 'NULL', which means that there is nothin surrounds the two protein names, so just write a space and a enter into file
				
			elif '-------------' in line:
				fout_sur_uni_sin.write(line)												#write the dividing line into file, too
		else:
			break

	fin_sin.close()
	fin_mul.close()
	fout_fea_term_list.close()
	fout_fea_term_set.close()
	fout_sur_uni_sin.close()
	fout_sur_uni_mul.close()

	path_fea_term_set = lower_path_VSM+'/'+'Feature_term_set.txt'							#path of the feature term set, for the construction of feature vector
		
	return path_fea_term_set, path_sur_uni_sin, path_sur_uni_mul							#return three paths for the next function

