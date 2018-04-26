from A_Train import Train
from B_Classification import Classification


def Train_ini(path_fea_vec_mul, path_count_mul):
	
	print 
	print '********************************************************************************'
	print 'start initialization of training...'
	print '********************************************************************************'
	print 
	
	clf_ini = Train.Train(path_count_mul, path_fea_vec_mul)

	return clf_ini

def Classify_ini(path_fea_vec_sin_CV, path_count_sin_CV, clf_ini):

	print 
	print '********************************************************************************'
	print 'start initialization of classification...'
	print '********************************************************************************'
	print 
	
	y_ment_ini = Classification.Classification(path_fea_vec_sin_CV, path_count_sin_CV, clf_ini)

	return y_ment_ini


