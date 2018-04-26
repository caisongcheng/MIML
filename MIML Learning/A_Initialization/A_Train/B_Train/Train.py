import numpy as np

from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

def Train(X_ment, y_ment_DS):
	print 	
	print '-------------------------------------------------------------'
	print 'start training a mention level classifier for initialization...'
	print 

	X = X_ment
	y = np.array(y_ment_DS)
	y = np.transpose(y_ment_DS)

	clf = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=10.0, fit_intercept=True, intercept_scaling=1)
	clf.fit(X, y)
	model = 'LR_mention_level_initialization.model'
	joblib.dump(clf, model)
