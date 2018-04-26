from __future__ import division
import os
import numpy as np
import csv
import copy

from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

def E_step(y_ment, ite):
	print 
	print '********************************************************************************'
	print 'start E step...'
	print '********************************************************************************'
	print 
	
#	y_ment = []

	os.chdir('CV')

	for direct in sorted(os.listdir('.')):
		os.chdir(direct)

		path_fea_vec_sin_CV = filter(lambda x: 'Feature_vector' in x, sorted(os.listdir('.')))[1]
		X_ment_sin_CV = np.loadtxt(path_fea_vec_sin_CV, dtype=int)

		model_mention = 'model_save/LR_mention_level_CV_'+str(ite)+'.model'
		clf_mention = joblib.load(model_mention)

		y_ment_sin_CV_proba = clf_mention.predict_proba(X_ment_sin_CV)

		model_tuple = '../../model_save/LR_tuple_level_CV_'+str(ite)+'.model'
		clf_tuple = joblib.load(model_tuple)
			
		path_count_sin_CV = filter(lambda x: 'Count' in x, sorted(os.listdir('.')))[1]
		fin = open(path_count_sin_CV, 'r')
		i = -1
		y_X_sin_CV = [[]]
		classification = 1
		y_ment_sin_CV_DS = []
		y_rela_sin_CV = []
		while True:
			line = fin.readline()
			if line:
				if '***' in line:
					i += 1
					if i != 0:
						y_X_sin_CV.append([])
					y_rela_sin_CV.append(classification)
				elif '------------' in line:
					classification = 0
				else:
					for j in range(int(line)):
						y_ment_sin_CV_DS.append(classification)
						y_X_sin_CV[i].append(classification)
			else:
				break
		fin.close()
	
		n = 0	
		for i in range(len(y_X_sin_CV)):
			for j in range(len(y_X_sin_CV[i])):
				y_X_sin_CV[i][j] = y_ment[int(direct)][n]
				n += 1

		calc_1 = []
		calc_0 = []
		n = 0
		for i in range(len(y_X_sin_CV)):
			for j in range(len(y_X_sin_CV[i])):
				num = 0
				for k in range(len(y_X_sin_CV[i])):
					if k != j:
						if y_X_sin_CV[i][k] == 1:
							num += 1
				X_sin_1 = round((num+1)/len(y_X_sin_CV[i]), 3)
				X_sin_0 = round(num/len(y_X_sin_CV[i]), 3)
				z_1 = y_ment_sin_CV_proba[n, 1] * pow(clf_tuple.predict_proba(X_sin_1)[0, y_rela_sin_CV[i]], 2)
				z_0 = y_ment_sin_CV_proba[n, 0] * pow(clf_tuple.predict_proba(X_sin_0)[0, y_rela_sin_CV[i]], 2)
			
				calc_1.append(str(y_ment_sin_CV_proba[n, 1])+'*'+'pow('+str(clf_tuple.predict_proba(X_sin_1)[0, y_rela_sin_CV[i]])+',2)'+'='+str(z_1))
				calc_0.append(str(y_ment_sin_CV_proba[n, 0])+'*'+'pow('+str(clf_tuple.predict_proba(X_sin_0)[0, y_rela_sin_CV[i]])+',2)'+'='+str(z_0))

				if z_1 >= z_0:
					y_X_sin_CV[i][j] = 1
				else:
					y_X_sin_CV[i][j] = 0
				n += 1

		y_ment_sin_CV = []	
		for i in range(len(y_X_sin_CV)):
			for j in range(len(y_X_sin_CV[i])):
				y_ment_sin_CV.append(y_X_sin_CV[i][j])

		y_ment[int(direct)] = np.array(y_ment_sin_CV)
#		y_ment.append(np.array(y_ment_sin_CV))


		if not os.path.exists('intermediate result'):
			os.mkdir('intermediate result')
		os.chdir('intermediate result')

		f_ment_CV = open('mention classification_CV.csv', 'a+')
		y_ment_CV_csv = csv.writer(f_ment_CV)
		y_ment_CV_csv.writerow(np.array(y_ment_sin_CV))
		f_ment_CV.close()

		f_E_step_CV = open('E-step calculation and comparison_CV.csv', 'a+')
		E_step_CV_csv = csv.writer(f_E_step_CV)
		E_step_CV_csv.writerow(calc_0)
		E_step_CV_csv.writerow(calc_1)
		E_step_CV_csv.writerow([])	
		f_E_step_CV.close()

		f_rela_ment_CV = open('relation_mention classification_CV.csv', 'a+')
		rela_ment_CV_csv = csv.writer(f_rela_ment_CV)
		rela_ment_CV_csv.writerow(y_X_sin_CV)
		f_rela_ment_CV.close()
		
	
		os.chdir('..')


		os.chdir('..')

	os.chdir('..')

	return y_ment





















