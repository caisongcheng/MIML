import os
import shutil

def divide(path_mul, path_part, k):
	


	sen_i = [[]]										#store interactive protein pairs and their sentences
	sen_ni = [[]]										#sotre non-interactice protein pairs and their sentences

################### read from text of multi folds used for training and store protein pairs and their senteces #####################

	fin_mul = open(path_mul, 'r')

	i = -1												#set i=-1 for the first iteracion
	#for j in range(3):
	while True:
		line = fin_mul.readline()
		if '-----------------' in line:					#if meet ---- in line, convert into reading non-interactives
			i = -1										#reset i=-1	to satisfy the iteration
			while True:
				line = fin_mul.readline()
				if line:
					if '***' in line:
						i += 1							#use i to locate the position of appended element in the list
						if i != 0:
							sen_ni.append([])			#if is not the first protein pair and meet ***, append a new element
						sen_ni[i].append(line)			#put non-interactive protein pair into [[]]
					else:
						sen_ni[i].append(line)			#put non-interactive sentence into [[]]
				else:
					break			
		else:
			if '***' in line:
				i += 1
				if i != 0:
					sen_i.append([])					#if is not the first protein pair and meet ***, append a new element
				sen_i[i].append(line)					#put interactive protein pair into [[]]
			else:
				sen_i[i].append(line)					#if not ***, put into interactives

		if not line:
			break

	fin_mul.close()

	#print len(sen_i)
	#print len(sen_ni)

	c = 0												#calculate c for validation
	for i in sen_i:
		#print len(i)
		c += len(i)
	for i in sen_ni:
		#print len(i)
		c += len(i)
	#print c

#####################################################################################################################################


############## divide protein pairs into several parts and try to make number of sentences of each part balanced # ##################

	pos_dlist = []										#store the numbers of nodes that divide interactive protein pairs into several parts
	neg_dlist = []										#store the numbers of nodes that divide non-interactive protein pairs into several parts
	for i in range(k):
		pos_dlist.append(i * len(sen_i) / k)			#calculate the numbers of nodes and append into list
	pos_dlist.append(len(sen_i))						#add (the number of last protein pair) +1 into list 
	for i in range(k):
		neg_dlist.append(i * len(sen_ni) / k)			#calculate the numbers of nodes and append into list
	neg_dlist.append(len(sen_ni))						#add (the number of last protein pair) +1 into list 

	for m in range(k):
		path_O = path_part+'/'+str(m)+'/'+os.path.splitext(os.path.basename(path_mul))[0]+'_'+str(m)+os.path.splitext(os.path.basename(path_mul))[1]
		fout = open(path_O, 'w+')							#reset num=0 for every iteraction
		for i in range(pos_dlist[m], pos_dlist[m+1]):
			for j in range(len(sen_i[i])):
				fout.write(sen_i[i][j])						#write every part of interactives into file
		fout.write("--------------------------------------dividing line for interactive and non-interactive protein pairs----------------------------------------------\n")
		for i in range(neg_dlist[m], neg_dlist[m+1]):
			for j in range(len(sen_ni[i])):
				fout.write(sen_ni[i][j])					#write every part of non-interactives into file
		fout.close()		
	
	for m in range(k):
		path_O = path_part+'/'+str(m)+'/'+os.path.splitext(os.path.basename(path_mul))[0]+'_'+str(m)+'-'+str(k)+os.path.splitext(os.path.basename(path_mul))[1]
		fout = open(path_O, 'w+')							#reset num=0 for every iteraction
		div_train = range(k)
		div_train.remove(m)
		for n in div_train:
			for i in range(pos_dlist[n], pos_dlist[n+1]):
				for j in range(len(sen_i[i])):
					fout.write(sen_i[i][j])					#write every part of interactives into file
		fout.write("--------------------------------------dividing line for interactive and non-interactive protein pairs----------------------------------------------\n")
		for n in div_train:
			for i in range(neg_dlist[n], neg_dlist[n+1]):
				for j in range(len(sen_ni[i])):
					fout.write(sen_ni[i][j])				#write every part of non-interactives into file
		fout.close()

#####################################################################################################################################

	

def divide_training_parts(low_dir_mer, k):
	print 
	print '-----------------------------------------------------------'
	print 'start dividing into parts of cross validation for training...'

	for direct_upper in low_dir_mer:
		for direct_lower in sorted(os.listdir(direct_upper)):
			if not os.path.exists(direct_upper+'/'+direct_lower+'/'+'CV'):
				os.mkdir(direct_upper+'/'+direct_lower+'/'+'CV')
			for i in range(k):
				if not os.path.exists(direct_upper + '/' + direct_lower + '/' + 'CV' + '/' + str(i)):
					os.mkdir(direct_upper + '/' + direct_lower + '/' + 'CV' + '/' + str(i))
			#if not os.path.exists(direct_upper+'/'+direct_lower+'/'+os.path.splitext(direct_file)[0]):
				#os.makedirs(direct_upper+'/'+direct_lower+'/'+os.path.splitext(direct_file)[0])
			#shutil.move(direct_upper+'/'+direct_lower+'/'+direct_file, direct_upper+'/'+direct_lower+'/'+os.path.splitext(direct_file)[0])

			path_mul = direct_upper+'/'+direct_lower+'/'+sorted(filter(lambda x: os.path.isfile(direct_upper+'/'+direct_lower+'/'+x), os.listdir(direct_upper+'/'+direct_lower)))[0]
			path_part = direct_upper + '/' + direct_lower + '/' + sorted(filter(lambda x: os.path.isdir(direct_upper+'/'+direct_lower+'/'+x), os.listdir(direct_upper+'/'+direct_lower)))[0]

			divide(path_mul, path_part, k)










				

