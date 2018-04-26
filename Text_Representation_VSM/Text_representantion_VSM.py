import os
import shutil

from A_Middle_unigram_fea import Middle_unigram_fea
from B_Surrounding_unigram_fea import Surrounding_unigram_fea
from C_Middle_Surrounding_unigram_fea import Middle_Surrounding_unigram_fea

class Text_Representation_VSM(object):											#this function is to represent the signatures by vector space model
	
	def __init__(self):
		print 
		print 'start Text Representation in VSM...\n'

	def Middle_unigram_fea(self, upper_path_pre, upper_path_VSM):
		Middle_unigram_fea.Middle_unigram_fea(upper_path_pre, upper_path_VSM)	

	def Surrounding_unigram_fea(self, upper_path_pre, upper_path_VSM):
		Surrounding_unigram_fea.Surrounding_unigram_fea(upper_path_pre, upper_path_VSM)	

	def Middle_Surrounding_unigram_fea(self, upper_path_pre, upper_path_VSM):
		Middle_Surrounding_unigram_fea.Middle_Surrounding_unigram_fea(upper_path_pre, upper_path_VSM)	


os.chdir('../Data')																#all the files are operated in /Data directory

TR = Text_Representation_VSM()													#instantiate a class of Text_Representation_VSM

pre_dir = 'Preprocess/Merge results'											#preprocessed reslult directory 
VSM_dir = 'VSM'																	#directory to store the result of text representation of vector space model 
'''dirs = ['Data', pre_dir, VSM_dir]
print dirs
def make_dir(target_dir):
	if not os.path.exists(target_dir):
		print 'make ',target_dir, ' directory...'	
		os.mkdir(target_dir)
	else:
		print target_dir, ' directory has existed...'
for direct in dirs:
	make_dir(direct)
print '----------------------------'  '''

pre_res_dir =  os.listdir(pre_dir)
print pre_res_dir
print '----------------------------'

for direct in pre_res_dir:
	if direct == 'unigram':																				#if there is a unigram, use VSM to represent the unigram result by call the unigram_fea function
		#TR.Middle_unigram_fea(pre_dir+'/'+direct, VSM_dir+'/'+'Middle_unigram')						#incoming parameter is the path of preprocess result and the path of VSM result
		#TR.Surrounding_unigram_fea(pre_dir+'/'+direct, VSM_dir+'/'+'Surrounding_unigram')				#incoming parameter is the path of preprocess result and the path of VSM result
		TR.Middle_Surrounding_unigram_fea(pre_dir+'/'+direct, VSM_dir+'/'+'Middle_Surrounding_unigram')				#incoming parameter is the path of preprocess result and the path of VSM result
		

'''fea_set = ['Middle_unigram', 'Surrounding_unigram']														#for now, fea_set is only two parts, used for merge feature set
fea_sel = [0, 1]																							#the list is for feature set selection, as 0 is for middle unigram, 1 is for surrounding unigram

#this step is for merge middle unigram and surrounding unigram feature sets
for direct in sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]])):
	if not os.path.exists(VSM_dir+'/'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'/'+direct):
		os.makedirs(VSM_dir+'/'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'/'+direct)
	for direct1 in sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct)):
		if not os.path.exists(VSM_dir+'/'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1):
			os.makedirs(VSM_dir+'/'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1)
		for direct2 in sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1)):
			if not os.path.exists(VSM_dir+'/'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1+'/'+direct2):
				os.makedirs(VSM_dir+'/'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1+'/'+direct2)
		
			shutil.copy(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2+'/'+filter(lambda x: 'Count' in x, sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2)))[1], VSM_dir+'/'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1+'/'+direct2)
			shutil.copy(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2+'/'+filter(lambda x: 'Count' in x, sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2)))[0], VSM_dir+'/'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1+'/'+direct2)

			fin_sin_0 = open(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2+'/'+filter(lambda x: 'Feature_vector' in x, sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2)))[1], 'r')
			fin_mul_0 = open(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2+'/'+filter(lambda x: 'Feature_vector' in x, sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2)))[0], 'r')
			fin_sin_1 = open(VSM_dir+'/'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1+'/'+direct2+'/'+filter(lambda x: 'Feature_vector' in x, sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1+'/'+direct2)))[1], 'r')
			fin_mul_1 = open(VSM_dir+'/'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1+'/'+direct2+'/'+filter(lambda x: 'Feature_vector' in x, sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1+'/'+direct2)))[0], 'r')
			fout_sin = open(VSM_dir+'/'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1+'/'+direct2+'/'+'Feature_vector_'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'_'+filter(lambda x: 'Feature_vector' in x, sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2)))[1].split('_')[-1], 'w+')
			fout_mul = open(VSM_dir+'/'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'/'+direct+'/'+direct1+'/'+direct2+'/'+'Feature_vector_'+fea_set[fea_sel[0]]+'+'+fea_set[fea_sel[1]]+'_'+filter(lambda x: 'Feature_vector' in x, sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2)))[0].split('_')[-2]+'_'+filter(lambda x: 'Feature_vector' in x, sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct+'/'+direct1+'/'+direct2)))[1].split('_')[-1], 'w+')


			#print filter(lambda x: 'Feature_vector' in x, sorted(os.listdir(VSM_dir+'/'+fea_set[fea_sel[0]]+'/'+direct)))[1]
			#for i in range(1):
			while True:
				line_sin_0 = fin_sin_0.readline()
				line_sin_1 = fin_sin_1.readline()
				if line_sin_0 and line_sin_1:
					print len(line_sin_0.split()+line_sin_1.split())
					fout_sin.write(' '.join(line_sin_0.split()+line_sin_1.split()) + '\n')
				elif not ((not line_sin_0) and (not line_sin_1)):
					print '\n\nError!!! Different number of samples.\n\n'
					break
				else:
					break
			
			while True:
				line_mul_0 = fin_mul_0.readline()
				line_mul_1 = fin_mul_1.readline()
				if line_mul_0 and line_mul_1:
					print len(line_mul_0.split()+line_mul_1.split())
					fout_mul.write(' '.join(line_mul_0.split()+line_mul_1.split()) + '\n')
				elif not ((not line_mul_0) and (not line_mul_1)):
					print '\n\nError!!! Different number of samples.\n\n'
					break
				else:
					break

			fin_sin_0.close()
			fin_mul_0.close()
			fin_sin_1.close()
			fin_mul_1.close()
			fout_sin.close()
			fout_mul.close()'''

	







