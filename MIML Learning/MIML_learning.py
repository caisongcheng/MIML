from __future__ import division
import os
import shutil
import numpy as np
import csv
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

'''from A_Loader import Loader
from B_Initialize_values import Initialize_values
from C_M_step import M_step
from D_E_step import E_step
from E_Validate import Validate'''

from A_Initialization import Initialization
from B_M_step import M_step
from C_E_step import E_step
from D_Validate import Validate

'''def First_iteration(X_ment, y_ment, y_X, y_rela, ite, y_ment_proba_csv, y_rela_csv, E_step_csv, X_rela_csv):
	y_ment_proba, clf, y_X = M_step.M_step(X_ment, y_ment, y_X, y_rela, ite, y_rela_csv, X_rela_csv)

	y_ment_proba_csv.writerow(y_ment_proba)

	y_X = E_step.E_step(y_ment_proba, clf, y_X, y_rela, E_step_csv)
	
	return y_X

def Next_iteration(X_ment, y_X, y_rela, ite, y_ment_csv, y_ment_proba_csv, y_rela_csv, E_step_csv, X_rela_csv):

	y_ment = []	
	for i in range(len(y_X)):
		for j in range(len(y_X[i])):
			y_ment.append(y_X[i][j])

	y_ment = np.array(y_ment)
	y_ment = np.transpose(y_ment)

	y_ment_csv.writerow(y_ment)

	y_ment_proba, clf, y_X = M_step.M_step(X_ment, y_ment, y_X, y_rela, ite, y_rela_csv, X_rela_csv)

	y_ment_proba_csv.writerow(y_ment_proba)

	y_X = E_step.E_step(y_ment_proba, clf, y_X, y_rela, E_step_csv)

	return y_X'''



os.chdir('../Data/VSM/')

VSM_path = ['Middle_unigram/', 'Surrounding_unigram/', 'Middle_Surrounding_unigram/']

VSM_path = ['Middle_Surrounding_unigram/']

for path in VSM_path:
	os.chdir(path)

	#for lower_path in sorted(os.listdir('.')):
	for lower_path in range(0, 1):
		lower_path = str(lower_path)

		os.chdir(lower_path)


		##########################   delete existed unuseful files and folders ##############################################

		if os.path.exists('intermediate result'):
			shutil.rmtree('intermediate result')
		if os.path.exists('model_save'):
			shutil.rmtree('model_save')

		os.chdir('CV')
		for direct in sorted(os.listdir('.')):
			os.chdir(direct)
			if os.path.exists('intermediate result'):
				shutil.rmtree('intermediate result')
			if os.path.exists('model_save'):
				shutil.rmtree('model_save')
			os.chdir('..')
		os.chdir('..')

		#####################################################################################################################


		##########################   initialization of training a mention level classifier   ################################

		path_fea_vec_mul = filter(lambda x: 'Feature_vector' in x, sorted(os.listdir('.')))[0]
		path_count_mul = filter(lambda x: 'Count' in x, sorted(os.listdir('.')))[0]
		clf_ini = Initialization.Train_ini(path_fea_vec_mul, path_count_mul)


		os.chdir('model_save')	
		model = 'LR_mention_level_initialization.model'
		clf_ini = joblib.load(model)
		os.chdir('..')

		#####################################################################################################################


		##########################   initialization of classifying every part of training data 		#########################

		y_ment_ini = []

		os.chdir('CV')
		
		for direct in sorted(os.listdir('.')):
		##for direct in range(0,1):
			## = str(direct)
			os.chdir(direct)

			path_fea_vec_sin_CV = filter(lambda x: 'Feature_vector' in x, sorted(os.listdir('.')))[1]
			path_count_sin_CV = filter(lambda x: 'Count' in x, sorted(os.listdir('.')))[1]
			y_ment_ini_CV = Initialization.Classify_ini(path_fea_vec_sin_CV, path_count_sin_CV, clf_ini)
			y_ment_ini.append(y_ment_ini_CV)

			os.chdir('..')

			os.chdir('..')
			if not os.path.exists('intermediate result'):
				os.mkdir('intermediate result')
			os.chdir('intermediate result')
			np.save('mention classification of initialization_'+direct+'.npy', y_ment_ini_CV)
			os.chdir('..')
			os.chdir('CV')

		os.chdir('..')


		os.chdir('intermediate result')
		for direct in sorted(os.listdir('../CV')):
			y_ment_ini.append(np.load('mention classification of initialization_'+direct+'.npy'))
		os.chdir('..')

		#####################################################################################################################


		##########################   start iteration of training		#####################################################

		y_ment = y_ment_ini

		ite_num = 10
		
		for ite in range(ite_num):

			print 
			print 'the ',ite,'th iteration..............'

			M_step.M_step(y_ment, ite)

			y_ment = E_step.E_step(y_ment, ite)

		#####################################################################################################################

		
		##########################   start iteration of testing			#####################################################

		for ite in range(ite_num):

			print 
			print 'the ',ite,'th iteration..............'
			
			Validate.Validate(ite)

		#####################################################################################################################


		os.chdir('..')

	os.chdir('..')























'''			X_ment_CV = []
			y_ment_CV = []

			for direct1 in sorted(os.listdir('.')):
			#for direct1 in range(0, 1):
				#direct1 = str(direct1)

				os.chdir(direct1)
				
				path_fea_vec_mul = filter(lambda x: 'Feature_vector' in x, sorted(os.listdir('.')))[0]
				path_count_mul = filter(lambda x: 'Count' in x, sorted(os.listdir('.')))[0]
				path_count_sin = filter(lambda x: 'Count' in x, sorted(os.listdir('.')))[1]
				path_fea_vec_sin = filter(lambda x: 'Feature_vector' in x, sorted(os.listdir('.')))[1]
				
				f_ment = open('mention classification.csv', 'wb')
				y_ment_csv = csv.writer(f_ment)

				f_rela = open('relation classification.csv', 'wb')
				y_rela_csv = csv.writer(f_rela)

				f_cross = open('relation_mention classification.csv', 'wb')
				y_cross_csv = csv.writer(f_cross)

				f_ment_proba = open('mention predict probability.csv', 'wb')
				y_ment_proba_csv = csv.writer(f_ment_proba)

				f_rela_proba = open('relation predict probability.csv', 'wb')
				f_rela_proba_csv = csv.writer(f_rela_proba)

				f_E_step = open('E-step calculation and comparison.csv', 'wb')
				E_step_csv = csv.writer(f_E_step)

				f_rela_fea_vec = open('input feature vector of relation classifier.csv', 'wb')
				X_rela_csv = csv.writer(f_rela_fea_vec)

				f_count_sen_num_pp = open('count on number of sentences(with pp).csv', 'wb')
				f_count_sen_num_pp_csv = csv.writer(f_count_sen_num_pp)
				f_count_sen_num = open('count on number of sentences(without pp).csv', 'wb')
				f_count_sen_num_csv = csv.writer(f_count_sen_num)

				#Load multiple feature vectors of sentences and classifications of protein pairs and original classifications of sentences and form a y_X(bridge). And all these are from training set	
				X_ment, y_rela, y_ment_DS, y_X = Loader.Loader(path_count_mul, path_fea_vec_mul, f_count_sen_num_csv, f_count_sen_num_pp_csv)

				f_count_sen_num.close()
				f_count_sen_num_pp.close()

				y_cross_csv.writerow(y_X)

				y_ment_csv.writerow(y_ment_DS)

				y_rela_csv.writerow(y_rela)

				y_ment_original = Initialize_values.Initialize_values(X_ment, y_ment_DS, y_ment_proba_csv)		#y_ment is a mat now
				print(metrics.classification_report(y_ment_DS, y_ment_original))
				print(metrics.confusion_matrix(y_ment_DS, y_ment_original))

				y_ment_csv.writerow(y_ment_original)

				f_ment.close()
				f_rela.close()
				f_cross.close()
				f_ment_proba.close()
				f_rela_proba.close()
				f_E_step.close()
				f_rela_fea_vec.close()

				X_ment_CV.append(X_ment)
				y_ment_CV.append(y_ment_original)

				os.chdir('..')

			for direct1 in sorted(os.listdir('.')):
				num = len(os.listdir('.'))
				X_ment = []

				os.chdir(direct1)
				
				for i in range(num):
					if i != int(direct1):
						X_ment.append(X_ment_CV[i])


				os.chdir('..')'''




			
'''			
			#print 'path_count_mul, path_fea_vec_mul', path_count_mul, path_fea_vec_mul
			#print 'path_count_sin, path_fea_vec_sin', path_count_sin, path_fea_vec_sin

			f_ment = open('mention classification.csv', 'wb')
			y_ment_csv = csv.writer(f_ment)

			f_rela = open('relation classification.csv', 'wb')
			y_rela_csv = csv.writer(f_rela)

			f_cross = open('relation_mention classification.csv', 'wb')
			y_cross_csv = csv.writer(f_cross)

			f_ment_proba = open('mention predict probability.csv', 'wb')
			y_ment_proba_csv = csv.writer(f_ment_proba)

			f_rela_proba = open('relation predict probability.csv', 'wb')
			f_rela_proba_csv = csv.writer(f_rela_proba)

			f_E_step = open('E-step calculation and comparison.csv', 'wb')
			E_step_csv = csv.writer(f_E_step)

			f_rela_fea_vec = open('input feature vector of relation classifier.csv', 'wb')
			X_rela_csv = csv.writer(f_rela_fea_vec)

			f_count_sen_num_pp = open('count on number of sentences(with pp).csv', 'wb')
			f_count_sen_num_pp_csv = csv.writer(f_count_sen_num_pp)
			f_count_sen_num = open('count on number of sentences(without pp).csv', 'wb')
			f_count_sen_num_csv = csv.writer(f_count_sen_num)

			#Load multiple feature vectors of sentences and classifications of protein pairs and original classifications of sentences and form a y_X(bridge). And all these are from training set	
			X_ment, y_rela, y_ment_DS, y_X = Loader.Loader(path_count_mul, path_fea_vec_mul, f_count_sen_num_csv, f_count_sen_num_pp_csv)

			f_count_sen_num.close()
			f_count_sen_num_pp.close()

			y_cross_csv.writerow(y_X)

			y_ment_csv.writerow(y_ment_DS)

			y_rela_csv.writerow(y_rela)

			y_ment_original = Initialize_values.Initialize_values(X_ment, y_ment_DS, y_ment_proba_csv)		#y_ment is a mat now
			print(metrics.classification_report(y_ment_DS, y_ment_original))
			print(metrics.confusion_matrix(y_ment_DS, y_ment_original))

			y_ment_csv.writerow(y_ment_original)

			n = 0
			for i in range(len(y_X)):
				for j in range(len(y_X[i])):
					y_X[i][j] = y_ment_original[n]
					n += 1
			y_cross_csv.writerow(y_X)

			ite = 0		
			y_X = First_iteration(X_ment, y_ment_original, y_X, y_rela, ite, y_ment_proba_csv, y_rela_csv, E_step_csv, X_rela_csv)

			y_cross_csv.writerow(y_X)

			ite = 15
			for it in range(1, ite):
				y_X = Next_iteration(X_ment, y_X, y_rela, it, y_ment_csv, y_ment_proba_csv, y_rela_csv, E_step_csv, X_rela_csv)
				y_cross_csv.writerow(y_X)

			f_ment.close()
			f_rela.close()
			f_cross.close()
			f_ment_proba.close()
			f_rela_proba.close()
			f_E_step.close()
			f_rela_fea_vec.close()

			f_ment_val = open('validation of mention classification.csv', 'wb')
			y_ment_val_csv = csv.writer(f_ment_val)

			f_cross_val = open('validation of relation_mention classification.csv', 'wb')
			y_cross_val_csv = csv.writer(f_cross_val)

			f_rela_fea_vec_val = open('validation of input feature vector of relation classifier.csv', 'wb')
			X_rela_val_csv = csv.writer(f_rela_fea_vec_val)

			f_rela_val = open('validation of relation classification.csv', 'wb')
			y_rela_val_csv = csv.writer(f_rela_val)

			f_cla_rep_val = open('validation of classification report.txt', 'w+')
			#cla_rep_val_csv = csv.writer(f_cla_rep_val)

			Validate.Validate(path_count_sin, path_fea_vec_sin, ite, y_ment_val_csv, y_cross_val_csv, X_rela_val_csv, y_rela_val_csv, f_cla_rep_val)

			f_ment_val.close()
			f_cross_val.close()
			f_rela_fea_vec_val.close()
			f_rela_val.close()
			f_cla_rep_val.close()'''



			
