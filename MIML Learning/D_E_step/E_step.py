from __future__ import division
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

def E_step(y_ment_proba, clf, y_X, y_rela, f_E_step_csv):
	print '****************************\n'
	print 'start E-step...'

	calc_1 = []
	calc_0 = []
	n = 0
	for i in range(len(y_X)):
		for j in range(len(y_X[i])):
			num = 0
			for k in range(len(y_X[i])):
				if k != j:
					if y_X[i][k] == 1:
						num += 1
			X_sin_1 = round((num+1)/len(y_X[i]), 3)
			X_sin_0 = round(num/len(y_X[i]), 3)
			z_1 = y_ment_proba[n, 1] * pow(clf.predict_proba(X_sin_1)[0, y_rela[i]], 2)
			z_0 = y_ment_proba[n, 0] * pow(clf.predict_proba(X_sin_0)[0, y_rela[i]], 2)
			
			calc_1.append(str(y_ment_proba[n, 1])+'*'+str(pow(clf.predict_proba(X_sin_1)[0, y_rela[i]], 2))+'='+str(z_1))
			calc_0.append(str(y_ment_proba[n, 0])+'*'+str(pow(clf.predict_proba(X_sin_0)[0, y_rela[i]], 2))+'='+str(z_0))

			if z_1 >= z_0:
				y_X[i][j] = 1
			else:
				y_X[i][j] = 0
			n += 1

	f_E_step_csv.writerow(calc_1)
	f_E_step_csv.writerow(calc_0)
	f_E_step_csv.writerow([])

	return y_X
