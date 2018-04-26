#-*-coding:utf-8-*-
"""这份代码主要是在师兄v6版本的基础上对分类器的参数进行了调整
      就是对dual参数进行了改变,dual参数当n_samples>n_features
   dual=False,否则dual=True
"""
import os
import shutil

from A_reduce_sentences import reduce_sentences
from B_randomize_sentences import randomize_sentences
from C_divide_parts import divide_parts
from D_linguistic_process import linguistic_process
from E_merge_parts import merge_parts
from F_divide_training_parts import divide_training_parts

#every function imported and called in the class is to produce file in the current directory

class Preprocess(object):

	def __init__(self):
		print 
		print '********************************************************************************'
		print 'start preprocess...'
		print '********************************************************************************'
		print 

	def reduce_sentences(self, path_tltp, path_red):
		reduce_sentences.reduce_sentences(path_tltp, path_red)						#reduce the number of sentences to less than 50

	def randomize_sentences(self, path_red, path_red_ran):
		randomize_sentences.randomize_sentences(path_red, path_red_ran)				#disturbe the order of protein pairs by randomizing the protein pairs(sentences belonged to protei pairs are not moved)
		
	def divide_parts(self, path_red_ran, n):
		path_divs = divide_parts.divide_parts(path_red_ran, n)						#divide the signatures into several parts
		return path_divs

	def linguistic_process(self, path_divs, ope):									#incoming parameters including path of division parts and the operation choice		
		ling = linguistic_process.linguistic_process(path_divs)						#instantiate a class linguistic_process, incoming parameter is the path of division parts

		top_dir_ling = 'Linguistic process results'									#make the directory Linguistic process results/, to store the result of linguistic process
		if not os.path.exists(top_dir_ling):
			os.mkdir(top_dir_ling)

		low_dir_ling = []															#make the lower directory, to store the different linguistic process result, middle_unigram(with pos tag, without), syntactic parsing, etc.
		low_dir_ling.append(top_dir_ling+'/unigram')
		low_dir_ling.append(top_dir_ling+'/unigram_POSTag')

		if not os.path.exists(low_dir_ling[ope]):
			os.makedirs(low_dir_ling[ope])

		if ope == 0:																#ope == 0 means to process middle unigram without pos tag
			ling.unigram(low_dir_ling[ope])
		elif ope == 1:																
			ling.unigram_POSTag(low_dir_ling[ope])									#ope == 0 means to process middle unigram with pos tag

		return low_dir_ling															#return the path of linguistic process result
		
	def merge_parts(self, low_dir_ling):											#merge the division parts into one, incomging parameters is the path of every linguistic result
		top_dir_mer = 'Merge results'												#make the top merge result directory
		if not os.path.exists(top_dir_mer):
			os.mkdir(top_dir_mer)

		low_dir_mer = []															
		for direct in low_dir_ling:													#store the lower path of corresponded merge result directory
			low_dir_mer.append(top_dir_mer+'/'+os.path.split(direct)[1])

		for direct in low_dir_mer:													#make the lower merge result directory  
			if not os.path.exists(direct):
				os.makedirs(direct)

		merge_parts.merge_parts(low_dir_ling, low_dir_mer)							#process of merging result of division parts after linguistic process
		return low_dir_mer
	
	def divide_training_parts(self, low_dir_mer, k):
		divide_training_parts.divide_training_parts(low_dir_mer, k)





pre = Preprocess()																	#instantiate the class Preprocess as pre

#all the files are operated in ../Data directory, e.g. all the data will be stored in top layer directory
if not os.path.exists('../Data/Preprocess'):										#make a ../Data/ directory, if it is not existed, and print a message, usually this will not happen
	os.makedirs('../Data/Preprocess')
	os.chdir('../Data/Preprocess')
else:										#if ../Data/ has existed, print the message
	os.chdir('../Data/Preprocess')

shutil.copy('../../Preprocess/True label true pattern sentences.txt', './')


############################################### preprocess of reduce sentences ######################################################

path_tltp = 'True label true pattern sentences.txt'									#path of the signature, yep, it is in the top directory, same as teh main file, so we do not need to give it any more dir
path_red = 'True label true pattern sentences_red.txt'								#path of the signature after reducing sentences, it is the same as the signature before any process
#pre.reduce_sentences(path_tltp, path_red)											#original process of reducing sentences, double # means it is not a total annotation, it is for test or sth

#####################################################################################################################################


############################################### preprocess of randomize sentences ####################################################

path_red_ran = 'True label true pattern sentences_red_ran.txt'						#path of the signature after randomizing protein pairs, it is the same as the signature before any process
#pre.randomize_sentences(path_red, path_red_ran)											#original process of randomizing protein pairs, double # means it is not a total annotation, it is for test or sth

#####################################################################################################################################


######################################## preprocess of dividing parts for cross validation for testing ##############################

#n = 5																				#number of folds for cross validation
#path_divs = pre.divide_parts(path_red_ran, n)										#original process of dividing signature into several parts, double # means it is not a total annotation, it is for test or sth

path_divs = ['True label true pattern sentences_red_ran_0.txt', 'True label true pattern sentences_red_ran_1.txt', 'True label true pattern sentences_red_ran_2.txt', 'True label true pattern sentences_red_ran_3.txt', 'True label true pattern sentences_red_ran_4.txt']
																					#this could not be concomitant with above statement, this is for convenient design

#####################################################################################################################################


############################################### preprocess of linguistic process ####################################################

ope = 0																			#ope is the operation choson, 0 for Middle_unigram, 1 for Middle_unigram_POSTag	
low_dir_ling = pre.linguistic_process(path_divs, ope)
##ope = 1
##low_dir_ling = pre.linguistic_process(path_divs, ope)
##low_dir_ling = ['Linguistic process results/unigram', 'Linguistic process results/unigram_POSTag']

low_dir_ling = ['Linguistic process results/unigram']								#this could not be concomitant with above statement, this is for convenient design, too.

#####################################################################################################################################


####################################### preprocess of merging parts for cross validation ############################################

low_dir_mer = pre.merge_parts(low_dir_ling)											#merge other parts into one, the one left is for test
low_dir_mer = ['Merge results/unigram']

#####################################################################################################################################


####################################### preprocess of cross validation for training #################################################

k = 5
pre.divide_training_parts(low_dir_mer, k)

#####################################################################################################################################




