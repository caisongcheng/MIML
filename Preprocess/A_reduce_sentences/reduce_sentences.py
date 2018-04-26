import random
import os

def reduce_sentences(path_I, path_O):					#reduce the number of sentences to less than 50
	print 
	print '-----------------------------------------------------------'
	print 'start reducing sentences...'

	sen_i = [[]]										#store interactive protein pairs and their sentences
	sen_ni = [[]]										#sotre non-interactice protein pairs and their sentences


    ####################### read from original text and store protein pairs and their senteces #################################

	file_tltp = open(path_I, 'r')
	i = -1												#set i=-1 for the first iteracion
	#for j in range(3):
	while True:
		line = file_tltp.readline()
		if '-----------------' in line:					#if meet ---- in line, convert into reading non-interactives
			i = -1										#reset i=-1		
			while True:
				line = file_tltp.readline()
				if line:
					if '***' in line:
						i += 1
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
	file_tltp.close()		

	print 
	print 'before reducing sentences:'
	print 'number of interactive protein pairs:', len(sen_i)
	print 'number of non-interactive protein pairs:', len(sen_ni)

	c = 0												#calculate c for validation
	for i in sen_i:
		#print len(i)
		c += len(i)
	for i in sen_ni:
		#print len(i)
		c += len(i)
	print 'number of all sentences:', c

	print 'number of all interactive sentences:', reduce(lambda x,y: x + y, map(lambda x: len(x)-1, sen_i))
	print 'number of all non-interactice sentences', reduce(lambda x,y: x + y, map(lambda x: len(x)-1, sen_ni))
	print 

    ###############################################################################################################################


	#################### reduce some interacitve and non-interacitve sentences to make training data balanced #####################e
	sen_i_bal = []

	for sen in filter(lambda x: 10>len(x)-1>1, sen_i):
		sen_i_bal.append(sen)

	num = len(filter(lambda x: 16>=len(x)-1>=10, sen_ni))
	sens = filter(lambda x: 16>=len(x)-1>=10, sen_i)
	for sen in random.sample(sens, num):
		sen_i_bal.append(sen)

	num = len(filter(lambda x: 44>=len(x)-1>=17, sen_ni))
	sens = filter(lambda x: 44>=len(x)-1>=17, sen_i)
	for sen in random.sample(sens, num):
		sen_i_bal.append(sen)

	num = len(filter(lambda x: 300>=len(x)-1>=45, sen_ni))
	sens = filter(lambda x: 300>=len(x)-1>=45, sen_i)
	for sen in random.sample(sens, num):
		sen_i_bal.append(sen)

	sen_ni_bal = []
	sens = filter(lambda x: len(x)-1>1, sen_ni)
	for sen in sens:
		sen_ni_bal.append(sen)

	''''print reduce(lambda x,y: x+y, map(lambda x: len(x)-1, filter(lambda x: len(x)-1>0, sen_i_bal)))
	print reduce(lambda x,y: x+y, map(lambda x: len(x)-1, filter(lambda x: len(x)-1>0, sen_ni_bal)))
	print

	print len(filter(lambda x: len(x)-1>0, sen_i_bal))
	print len(filter(lambda x: len(x)-1>0, sen_ni_bal))
	print

	print len(sen_i_bal)
	print len(sen_ni_bal)
	print'''
	#############################################################################################################################


	######################## write interactice and non-interactive senteces into balanced signature #############################
	fout = open(path_O, 'w+')
	for i in range(len(sen_i_bal)):
		for j in range(len(sen_i_bal[i])):
			fout.write(str(sen_i_bal[i][j]))
	fout.write('------------------------------------- dividing line for interactive and non-interactive protein pairs ---------------------------------------------\n')
	for i in range(len(sen_ni_bal)):
		for j in range(len(sen_ni_bal[i])):
			fout.write(str(sen_ni_bal[i][j]))
	fout.close()
	#############################################################################################################################


    ####################### reserve all non-interactive sentences, reduce some interactive sentences #################################

	'''file_O = open(path_O, 'w+')

	for i in range(len(sen_i)):		
		file_O.write(str(sen_i[i][0]))					#first, write protein pair into file
		del sen_i[i][0]									#then, del protein pair from the list
		if len(sen_i[i]) > 10:							#if number of sentences of one protein pair is more than 50
			random.shuffle(sen_i[i])					#first random sentences
			r = random.randint(10,10)					#select those protein pairs by the probability of a quarter 
			for j in range(r):	#about a quarter of sentences are disposed like this
				file_O.write(str(sen_i[i][j]))
		else:											#other protein pairs are not disposed
			for j in range(len(sen_i[i])):
				file_O.write(str(sen_i[i][j]))'''


	'''for i in range(len(sen_i)):		
		file_O.write(str(sen_i[i][0]))					#first, write protein pair into file
		del sen_i[i][0]									#then, del protein pair from the list
		if len(sen_i[i]) > 50:							#if number of sentences of one protein pair is more than 50
			random.shuffle(sen_i[i])					#first random sentences
			r = random.randint(1,4)						#select those protein pairs by the probability of a quarter 
			if r == 1:
				for j in range(random.randint(11,50)):	#about a quarter of sentences are disposed like this
					file_O.write(str(sen_i[i][j]))
			else:
				for j in range(random.randint(1,10)):	#about three quarters of sentences are disposed like this
					file_O.write(str(sen_i[i][j]))
		elif 5 < len(sen_i[i]) <= 40:					#protein pairs whose number of sentences like this are disposed like this
			random.shuffle(sen_i[i])
			for j in range(random.randint(1,5)):
				file_O.write(str(sen_i[i][j]))
		elif 40 < len(sen_i[i]) <= 50:					#protein pairs whose number of sentences like this are disposed like this
			random.shuffle(sen_i[i])
			for j in range(random.randint(6,10)):
				file_O.write(str(sen_i[i][j]))
		else:											#other protein pairs are not disposed
			for j in range(len(sen_i[i])):
				file_O.write(str(sen_i[i][j]))'''
		
	'''file_O.write('--------------------------------------dividing line for interactive and non-interactive proteinpairs----------------------------------------------\n')

	for i in range(len(sen_ni)):
		file_O.write(str(sen_ni[i][0]))
		del sen_ni[i][0]
		for j in range(len(sen_ni[i])):
			file_O.write(str(sen_ni[i][j]))'''

	'''for i in range(len(sen_ni)):
		file_O.write(str(sen_ni[i][0]))
		del sen_ni[i][0]
		if len(sen_ni[i]) > 50:							#for non-interactive protein pairs, only those whose number of sentences are more than 50 will be disposed like this(hehe, too lazy too discribe)
			random.shuffle(sen_ni[i])
			for j in range(random.randint(11,50)):
				file_O.write(str(sen_ni[i][j]))
		else:											#for other non-interactive protein pairs, they are not disposed
			for j in range(len(sen_ni[i])):
				file_O.write(str(sen_ni[i][j]))'''

	'''file_O.close()'''

	#################################################################################################################################


	########################## check for confirming number of interactive and non-interactive sentences #############################

	sen_i_red = [[]]
	sen_ni_red = [[]]

	file_ch = open(path_O, 'r')
	i = -1												#set i=-1 for the first iteracion
	#for j in range(3):
	while True:
		line = file_ch.readline()
		if '-----------------' in line:					#if meet ---- in line, convert into reading non-interactives
			i = -1										#reset i=-1		
			while True:
				line = file_ch.readline()
				if line:
					if '***' in line:
						i += 1
						if i != 0:
							sen_ni_red.append([])			#if is not the first protein pair and meet ***, append a new element
						sen_ni_red[i].append(line)			#put non-interactive protein pair into [[]]
					else:
						sen_ni_red[i].append(line)			#put non-interactive sentence into [[]]
				else:
					break
			
		else:
			if '***' in line:
				i += 1
				if i != 0:
					sen_i_red.append([])					#if is not the first protein pair and meet ***, append a new element
				sen_i_red[i].append(line)					#put interactive protein pair into [[]]
			else:
				sen_i_red[i].append(line)					#if not ***, put into interactives

		if not line:
			break
	file_ch.close()		

	print 'after reducing sentences:'
	print 'number of interactive protein pairs:', len(sen_i_red)
	print 'number of non-interactive protein pairs:', len(sen_ni_red)

	c = 0												#calculate c for validation
	for i in sen_i_red:
		#print len(i)
		c += len(i)
	for i in sen_ni_red:
		#print len(i)
		c += len(i)
	print 'number of all sentences:', c

	print 'number of all interactive sentences:', reduce(lambda x,y: x + y, map(lambda x: len(x)-1, sen_i_red))
	print 'number of all non-interactice sentences', reduce(lambda x,y: x + y, map(lambda x: len(x)-1, sen_ni_red))
	print 
	
	############################################################################################################################

	
if __name__=="__main__":
	print 'executable script... ...'
	os.chdir('../../Data/Preprocess')

	#reduce_sentences('True label true pattern sentences_red.txt', 'True label true pattern sentences_red_test_test.txt')

	reduce_sentences('True label true pattern sentences.txt', 'True label true pattern sentences_red_test.txt')














