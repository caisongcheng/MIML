from __future__ import division
import os 
import numpy as np
import csv

from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


def Train_ment(y_ment, ite):
	print 	
	print '-------------------------------------------------------------'
	print 'start training several mention level classifiers...'
	print 

	os.chdir('CV')

	for direct in sorted(os.listdir('.')):
	##for direct in range(0,1):
		##direct = str(direct)

		X_ment_sin = []

		for direct1 in sorted(os.listdir('.')):
			if direct1 != direct:
				os.chdir(direct1)

				path_fea_vec_sin_CV = filter(lambda x: 'Feature_vector' in x, sorted(os.listdir('.')))[1]
				X_ment_sin_CV = np.loadtxt(path_fea_vec_sin_CV, dtype=int)

				X_ment_sin.append(X_ment_sin_CV)

				os.chdir('..')

		X_ment_mul_CV = reduce(lambda x,y:np.concatenate((x,y)), X_ment_sin)


		os.chdir(direct)

		y_ment_mul_CV = np.array([])
		for m in range(len(sorted(os.listdir('..')))):
			if m != int(direct):
				print m
				y_ment_mul_CV = np.append(y_ment_mul_CV, y_ment[m])

		clf_mention = LogisticRegression(penalty='l2', dual=True, tol=0.0001, C=10.0, fit_intercept=True, intercept_scaling=1)
		clf_mention.fit(X_ment_mul_CV, y_ment_mul_CV)

		print  'classification report:'
		print(metrics.classification_report(y_ment_mul_CV, clf_mention.predict(X_ment_mul_CV)))
		print 'confusion matrix:'
		print(metrics.confusion_matrix(y_ment_mul_CV, clf_mention.predict(X_ment_mul_CV)))

		if not os.path.exists('model_save'):
			os.mkdir('model_save')
		os.chdir('model_save')		
		model_mention = 'LR_mention_level_CV_'+str(ite)+'.model'
		joblib.dump(clf_mention, model_mention)	
		os.chdir('..')


		os.chdir('..')


	os.chdir('..')


def Train_tuple(y_ment, ite):
	print 	
	print '-------------------------------------------------------------'
	print 'start training a tuple level classifier...'
	print 

	y_ment_mul = np.array([])
	for m in range(len(sorted(os.listdir('CV')))):
		y_ment_mul = np.append(y_ment_mul, y_ment[m])


	y_rela = []				#list
	y_X = [[]]				#list


	os.chdir('CV')

	for direct in sorted(os.listdir('.')):
		os.chdir(direct)

		path_count_sin_CV = filter(lambda x: 'Count' in x, sorted(os.listdir('.')))[1]
		f_count_sin_CV = open(path_count_sin_CV, 'r')

		y_rela_CV = []
		y_X_CV = [[]]
		i = -1
		classification = 1

		while True:
			line = f_count_sin_CV.readline()
			if line:
				if '***' in line:
					i += 1
					if i != 0:
						y_X_CV.append([])
					#y_X[i].append(line)
					y_rela_CV.append(classification)
				elif '-------------' in line:
					classification = 0
				else:
					for j in range(int(line)):
						y_X_CV[i].append(classification)
			else:
				break

		f_count_sin_CV.close()

		y_rela.extend(y_rela_CV)
		y_X.extend(y_X_CV)

		os.chdir('..')

	os.chdir('..')

	del y_X[0]

	n = 0
	for i in range(len(y_X)):
		for j in range(len(y_X[i])):
			y_X[i][j] = y_ment_mul[n]
			n += 1

	X_rela = []
	for y in y_X:
		num = 0
		for y_x in y:
			if y_x == 1:
				num += 1
		X_rela.append(round(num/len(y), 3))
	X_rela = np.matrix(X_rela)
	X_rela = np.transpose(X_rela)

	clf_tuple = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=10.0, fit_intercept=True, intercept_scaling=1)
	clf_tuple.fit(X_rela, y_rela)

	if not os.path.exists('model_save'):
		os.mkdir('model_save')
	os.chdir('model_save')	

	model_tuple = 'LR_tuple_level_CV_'+str(ite)+'.model'
	joblib.dump(clf_tuple, model_tuple)	

	os.chdir('..')


	if not os.path.exists('intermediate result'):
		os.mkdir('intermediate result')
	os.chdir('intermediate result')

	f_y_rela = open('actual relation classification.csv', 'a+')
	y_rela_csv = csv.writer(f_y_rela)
	y_rela_csv.writerow(y_rela)
	f_y_rela.close()

	f_X_rela = open('relation fit input.csv', 'a+')
	X_rela_csv = csv.writer(f_X_rela)
	X_rela_csv.writerow(X_rela)
	f_X_rela.close()

	f_rela_proba = open('predict relation probability.csv', 'a+')
	rela_proba_csv = csv.writer(f_rela_proba)
	rela_proba_csv.writerow(clf_tuple.predict_proba(X_rela))
	f_rela_proba.close()

	f_rela_pred = open('predict relation classification.csv', 'a+')
	rela_pred_csv = csv.writer(f_rela_pred)
	rela_pred_csv.writerow(clf_tuple.predict(X_rela))
	f_rela_pred.close()

	f_rela_ment = open('relation_mention classification.csv', 'a+')
	rela_ment_csv = csv.writer(f_rela_ment)
	rela_ment_csv.writerow(y_X)
	f_rela_ment.close()

	os.chdir('..')


	print 'classification report:'
	print(metrics.classification_report(y_rela, clf_tuple.predict(X_rela)))
	print 'confusion matrix:'
	print(metrics.confusion_matrix(y_rela, clf_tuple.predict(X_rela)))




def M_step(y_ment, ite):
	print 
	print '********************************************************************************'
	print 'start M step...'
	print '********************************************************************************'
	print 

	Train_ment(y_ment, ite)

	Train_tuple(y_ment, ite)

	
	




