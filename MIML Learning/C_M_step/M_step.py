from __future__ import division
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import os

def Train_ment_model(X, y, i):
	print '----------------------------'
	print 'start training mention-level model for the '+str(i)+'th time...'
	clf = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=10.0, fit_intercept=True, intercept_scaling=1)
	print clf		
	clf.fit(X, y)

	model = 'LR_mention_level_'+str(i)+'.model'
	os.chdir("model_save")
	joblib.dump(clf, model)
	os.chdir("..")
		
	'''print 'start predicting\n'
	expected = y
	predicted = clf.predict(X)
	print(metrics.classification_report(expected, predicted))
	print(metrics.confusion_matrix(expected, predicted))
	
	if not os.path.exists('mention_level_results'):
		os.mkdir('mention_level_results')
	os.chdir('mention_level_results')
	np.savetxt('predict_proba_'+ite+'.txt', clf.predict_proba(X), fmt="%.3f")
	np.savetxt('predicted_'+ite+'.txt', predicted, fmt="%d")
	os.chdir('..')'''

	return clf.predict_proba(X)

def Train_rela_model(X, y, i, y_rela_csv):
	print '----------------------------'
	print 'start training relation-level model...'
	clf = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=10.0, fit_intercept=True, intercept_scaling=1)
	print clf		
	clf.fit(X, y)

	model = 'LR_relation_level_'+str(i)+'.model'
	os.chdir("model_save")
	joblib.dump(clf, model)
	os.chdir("..")
		
	print 'start predicting\n'
	expected = y
	predicted = clf.predict(X)
	print(metrics.classification_report(expected, predicted))
	print(metrics.confusion_matrix(expected, predicted))

	y_rela_csv.writerow(predicted)

	'''if not os.path.exists('relation_level_results'):
		os.mkdir('relation_level_results')
	os.chdir('relation_level_results')
	np.savetxt('predict_proba_'+ite+'.txt', clf.predict_proba(X), fmt="%.3f")
	np.savetxt('predicted_'+ite+'.txt', predicted, fmt="%d")
	os.chdir('..')'''

	return clf

def M_step(X_ment, y_ment, y_X, y_rela, ite, y_rela_csv, X_rela_csv):
	print '****************************\n'
	print 'start M-step...'

	y_ment_proba = Train_ment_model(X_ment, y_ment, ite)	

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

	X_rela_csv.writerow(X_rela)

	clf = Train_rela_model(X_rela, y_rela, ite, y_rela_csv)

	return y_ment_proba, clf, y_X
