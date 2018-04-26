import numpy as np
import os

from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

def Loader(path_count_mul, path_fea_vec_mul):
	print 	
	print '-------------------------------------------------------------'
	print 'start loading feature vector and classifications...'
	print 

	X_ment = np.loadtxt(path_fea_vec_mul, dtype=int)		#matrix
	
	y_ment = []				#list
	i = -1
	classification = 1
	fin = open(path_count_mul, 'r')
	while True:
		line = fin.readline()
		if line:
			if '***' in line:
				pass
			elif '-------------' in line:
				classification = 0
			else:
				for j in range(int(line)):
					y_ment.append(classification)
		else:
			break


	print X_ment.shape
	print len(y_ment)

	return X_ment, y_ment


def Train_mention_level_classifier(X_ment, y_ment_DS):
	print 	
	print '-------------------------------------------------------------'
	print 'start training a mention level classifier for initialization...'
	print 

	X = X_ment
	y = np.array(y_ment_DS)
	y = np.transpose(y_ment_DS)

	clf = LogisticRegression(penalty='l2', dual=True, tol=0.0001, C=10.0, fit_intercept=True, intercept_scaling=1)
	clf.fit(X, y)

	if not os.path.exists('model_save'):
		os.mkdir('model_save')
	os.chdir('model_save')	
	
	model = 'LR_mention_level_initialization.model'
	joblib.dump(clf, model)

	os.chdir('..')

	print 'classification report:'
	print(metrics.classification_report(y, clf.predict(X)))
	print 'confusion matrix:'
	print(metrics.confusion_matrix(y, clf.predict(X)))

	return clf


def Train(path_count_mul, path_fea_vec_mul):
	#Load multiple feature vectors of sentences and classifications of protein pairs and original classifications of sentences and form a y_X(bridge). And all these are from training set	
	X_ment, y_ment_DS = Loader(path_count_mul, path_fea_vec_mul)

	clf_ini = Train_mention_level_classifier(X_ment, y_ment_DS)

	return clf_ini


