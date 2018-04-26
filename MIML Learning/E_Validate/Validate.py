from __future__ import division
import os
import numpy as np
import csv
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

def Predict_mention(X, model):
	os.chdir('model_save')
	clf = joblib.load(model)
	predicted = clf.predict(X)
	os.chdir('..')
	return predicted

def Predict_relation(X, y, model, f_cla_rep_val):
	os.chdir('model_save')
	clf = joblib.load(model)
	expected = y
	predicted = clf.predict(X)
	os.chdir('..')
	print 'classification report:'
	print(metrics.classification_report(expected, predicted))
	print 'confusion matrix:'
	print(metrics.confusion_matrix(expected, predicted))

	f_cla_rep_val.write('classification report:\n')
	f_cla_rep_val.write(metrics.classification_report(expected, predicted))
	f_cla_rep_val.write('\n')
	f_cla_rep_val.write('confusion matrix:\n')
	cla_rep_val_csv = csv.writer(f_cla_rep_val)
	cla_rep_val_csv.writerows(metrics.confusion_matrix(expected, predicted))
	f_cla_rep_val.write('\n\n')

	return predicted

def Validate(path_count_sin, path_fea_vec_sin, itera, y_ment_val_csv, y_cross_val_csv, X_rela_val_csv, y_rela_val_csv, f_cla_rep_val):
	print '****************************\n'
	print 'start valadation...'

	X_ment = np.loadtxt(path_fea_vec_sin, dtype=int)

	fin = open(path_count_sin, 'r')
	i = -1
	y_X = [[]]
	classification = 1
	y_ment_DS = []
	y_rela = []
	while True:
		line = fin.readline()
		if line:
			if '***' in line:
				i += 1
				if i != 0:
					y_X.append([])
				y_rela.append(classification)
			elif '------------' in line:
				classification = 0
			else:
				for j in range(int(line)):
					y_ment_DS.append(classification)
					y_X[i].append(classification)
		else:
			break
	fin.close()

	#print X_ment.shape
	#print len(y_X)
#print len(y_rela)
#print len(y_ment)

	y_ment_val_csv.writerow(y_ment_DS)

	y_rela_val_csv.writerow(y_rela)

	y_rela = np.matrix(y_rela)
	y_rela = np.transpose(y_rela)

	for ite in range(itera):
		model_mention = 'LR_mention_level_' + str(ite) + '.model'
		model_relation = 'LR_relation_level_' +str(ite) + '.model'
		y_ment = Predict_mention(X_ment, model_mention)

		y_ment_val_csv.writerow(y_ment)
	
		n = 0
		for i in range(len(y_X)):
			for j in range(len(y_X[i])):
				y_X[i][j] = y_ment[n]
				n += 1

		y_cross_val_csv.writerow(y_X)
	#	print n
	#	print len(y_ment)
	#	print len(y_X)

		X_rela = []
		for y in y_X:
			num = 0
			for y_x in y:
				if y_x == 1:
					num += 1
			X_rela.append(round(num/len(y), 3))

		X_rela_val_csv.writerow(X_rela)

		X_rela = np.matrix(X_rela)
		X_rela = np.transpose(X_rela)

		predict_y_rela = Predict_relation(X_rela, y_rela, model_relation, f_cla_rep_val)

		y_rela_val_csv.writerow(predict_y_rela)

if __name__ == '__main__':
	os.chdir('../Data/VSM_results/Middle_unigram/0/')
	Validate('Count_Middle_unigram_0.txt', 'Feature_vector_Middle_unigram_0.txt', 5)

