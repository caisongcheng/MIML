from __future__ import division
import os 
import numpy as np
import csv

from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


def ment_cla(ite):
	path_fea_vec_sin = filter(lambda x: 'Feature_vector' in x, sorted(os.listdir('.')))[1]
	X_ment_sin = np.loadtxt(path_fea_vec_sin, dtype=int)
	
	clf_ment_CV = []

	os.chdir('CV')
	for direct in sorted(os.listdir('.')):
		os.chdir(direct)
		
		os.chdir('model_save')

		model_ment_CV = 'LR_mention_level_CV_'+str(ite)+'.model'
		clf_ment_CV.append(joblib.load(model_ment_CV))

		os.chdir('..')

		os.chdir('..')

	div_num = len(sorted(os.listdir('.')))

	os.chdir('..')

	clf_ment = clf_ment_CV[0].predict_proba(X_ment_sin)
	for i in range(div_num):
		if i != 0:
			clf_ment += clf_ment_CV[i].predict_proba(X_ment_sin)

	y_ment = []
	for i in range(len(clf_ment)):
		if clf_ment[i,0] > clf_ment[i,1]:
			y_ment.append(0)
		else:
			y_ment.append(1)

	print 
	print 'test predict properly:', clf_ment[0,0]+clf_ment[0,1]
	print 

	os.chdir('intermediate result')
	if not os.path.exists('Validation'):
		os.mkdir('Validation')
	os.chdir('Validation')
	f_ment_val = open('validation of predict mention classification.csv', 'a+')
	y_ment_val_csv = csv.writer(f_ment_val)
	y_ment_val_csv.writerow(y_ment)
	f_ment_val.close()
	os.chdir('..')
	os.chdir('..')


	return y_ment
		

def rela_cla(y_ment, ite):
	path_count_sin = filter(lambda x: 'Count' in x, sorted(os.listdir('.')))[1]
	f_count_sin = open(path_count_sin, 'r')

	y_rela = []				#list
	y_X = [[]]				#list
	i = -1
	classification = 1

	while True:
		line = f_count_sin.readline()
		if line:
			if '***' in line:
				i += 1
				if i != 0:
					y_X.append([])
				#y_X[i].append(line)
				y_rela.append(classification)
			elif '-------------' in line:
				classification = 0
			else:
				for j in range(int(line)):
					y_X[i].append(classification)
		else:
			break

	f_count_sin.close()

	
	n = 0
	for i in range(len(y_X)):
		for j in range(len(y_X[i])):
			y_X[i][j] = y_ment[n]
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

	os.chdir('model_save')
	model_tuple = 'LR_tuple_level_CV_'+str(ite)+'.model'
	clf_tuple = joblib.load(model_tuple)
	os.chdir('..')

	print 'classification report:'
	print(metrics.classification_report(y_rela, clf_tuple.predict(X_rela)))
	print 'confusion matrix:'
	print(metrics.confusion_matrix(y_rela, clf_tuple.predict(X_rela)))


	os.chdir('intermediate result')
	if not os.path.exists('Validation'):
		os.mkdir('Validation')
	os.chdir('Validation')

	f_ment_rela_val = open('validation of relation_mention classification.csv', 'a+')
	y_ment_rela_val_csv = csv.writer(f_ment_rela_val)
	y_ment_rela_val_csv.writerow(y_X)
	f_ment_rela_val.close()

	f_X_rela_val = open('validation of relation fit input.csv', 'a+')
	X_rela_val_csv = csv.writer(f_X_rela_val)
	X_rela_val_csv.writerow(X_rela)
	f_X_rela_val.close()

	f_y_rela_val = open('validation of predict relation classification.csv', 'a+')
	y_rela_val_csv = csv.writer(f_y_rela_val)
	y_rela_val_csv.writerow(clf_tuple.predict(X_rela))
	f_y_rela_val.close()

	f_cla_report_val = open('validation of classification reportand confusion matrix.txt', 'a+')
	f_cla_report_val.write('the '+str(ite)+'th time\n')
	f_cla_report_val.write('classification report:\n')
	f_cla_report_val.write(metrics.classification_report(y_rela, clf_tuple.predict(X_rela)))
	f_cla_report_val.write('\n')
	f_cla_report_val.write('confusion matrix:\n')
	cla_report_val_csv = csv.writer(f_cla_report_val)
	cla_report_val_csv.writerows(metrics.confusion_matrix(y_rela, clf_tuple.predict(X_rela)))
	f_cla_report_val.write('\n\n')
	f_cla_report_val.close()

	os.chdir('..')
	os.chdir('..')


def Validate(ite):
	print 
	print '********************************************************************************'
	print 'start validating...'
	print '********************************************************************************'
	print 

	y_ment = ment_cla(ite)
	rela_cla(y_ment, ite)










