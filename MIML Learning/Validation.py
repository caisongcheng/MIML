import os
import numpy as np
from sklearn import metrics

from A_Loader import Loader
from B_Initialize_values import Initialize_values
from C_M_step import M_step
from D_E_step import E_step
from E_Validate import Validate

def First_iteration(X_ment, y_ment, y_X, y_rela, ite):
	y_ment_proba, clf, y_X = M_step.M_step(X_ment, y_ment, y_X, y_rela, ite)
	y_X = E_step.E_step(y_ment_proba, clf, y_X, y_rela)
	
	return y_X

def Next_iteration(X_ment, y_X, y_rela, ite):

	y_ment = []	
	for i in range(len(y_X)):
		for j in range(len(y_X[i])):
			y_ment.append(y_X[i][j])

	y_ment = np.array(y_ment)
	y_ment = np.transpose(y_ment)

	y_ment_proba, clf, y_X = M_step.M_step(X_ment, y_ment, y_X, y_rela, ite)
	y_X = E_step.E_step(y_ment_proba, clf, y_X, y_rela)

	return y_X


#If Data not exists(usually impossible), create it; then chanege directory into Data/
#if not os.path.exists('Data/VSM_results/'):
#		os.makedirs('Data/VSM_results/')
os.chdir('Data/VSM_results/')

#remove the useless files
VSM_path = []
VSM_path.append('Middle_unigram/')
for path in VSM_path:
	os.chdir(path)
	for i in range(len(os.listdir('.'))):
		for f in os.listdir(str(i)):
			if 'Feature_term' in f or 'Sequence' in f:
				os.remove(str(i)+'/'+f)
	os.chdir('..')


for path in VSM_path:
	os.chdir(path)

	for lower_path in sorted(os.listdir('.')):
	#for lower_path in range(1):
		#lower_path = str(lower_path)

		os.chdir(lower_path)
		print lower_path
		path_count_mul = sorted(os.listdir('.'))[0]
		path_count_sin = sorted(os.listdir('.'))[1]
		path_fea_vec_mul = sorted(os.listdir('.'))[2]
		path_fea_vec_sin = sorted(os.listdir('.'))[3]
		print path_count_mul, path_fea_vec_mul

		ite = 5
		
		Validate.Validate(path_count_sin, path_fea_vec_sin, ite)	

		os.chdir('..')

	os.chdir('..')		









