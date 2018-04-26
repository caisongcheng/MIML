import numpy as np

from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


def Loader(path_fea_vec_sin_CV, path_count_sin_CV):
	print 	
	print '-------------------------------------------------------------'
	print 'start loading feature vector and classifications...'
	print 

	X_ment = np.loadtxt(path_fea_vec_sin_CV, dtype=int)		#matrix
	
	fin = open(path_count_sin_CV, 'r')
	i = -1
	classification = 1
	y_ment_DS = []
	while True:
		line = fin.readline()
		if line:
			if '***' in line:
				pass
			elif '------------' in line:
				classification = 0
			else:
				for j in range(int(line)):
					y_ment_DS.append(classification)
		else:
			break
	fin.close()

	return X_ment, y_ment_DS

def Classify(X_ment, y_ment_DS, clf_ini):
	print 	
	print '-------------------------------------------------------------'
	print 'start classifying mentions...'
	print 

	expected = y_ment_DS
	predicted = clf_ini.predict(X_ment)

	print  'classification report:'
	print(metrics.classification_report(expected, predicted))
	print 'confusion matrix:'
	print(metrics.confusion_matrix(expected, predicted))

	return predicted

def Classification(path_fea_vec_sin_CV, path_count_sin_CV, clf_ini):
	print 	
	print '-------------------------------------------------------------'
	print 'start classifying mentions for initialization...'
	print 

	X_ment, y_ment_DS = Loader(path_fea_vec_sin_CV, path_count_sin_CV)

	y_ment_ini = Classify(X_ment, y_ment_DS, clf_ini)

	return y_ment_ini

	

	











