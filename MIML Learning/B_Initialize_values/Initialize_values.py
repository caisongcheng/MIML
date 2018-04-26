from __future__ import division
import numpy as np
import os
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

def Train_ment_model(X, y, y_ment_proba_csv):
	print '----------------------------'
	print 'start training mention-level model for initialization...'
	
	clf = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=10.0, fit_intercept=True, intercept_scaling=1)
	print clf		
	
	clf.fit(X, y)

	y_ment_proba_csv.writerow(clf.predict_proba(X))

	model = 'LR_mention_level_original.model'
	if not os.path.exists('model_save'):
		os.mkdir('model_save')
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

	return clf.predict(X)

def Initialize_values(X_ment, y_ment, y_ment_proba_csv):
	print '****************************\n'
	print 'start initializing values..'

	X = X_ment
	y = np.array(y_ment)
	y = np.transpose(y_ment)

	y_ment = Train_ment_model(X, y, y_ment_proba_csv)
	
	return y_ment
