import random

def randomize_sentences(path_I, path_O):
	print 
	print '-----------------------------------------------------------'
	print 'start randomizing sentences...'
		
	sen_i = [[]]										#store interactive protein pairs and their sentences
	sen_ni = [[]]										#sotre non-interactice protein pairs and their sentences

###################### read from text after reducing sentences and store protein pairs and their senteces ##########################

	file_red = open(path_I, 'r')

	i = -1												#set i=-1 for the first iteracion
	#for j in range(3):
	while True:
		line = file_red.readline()
		if '-----------------' in line:					#if meet ---- in line, convert into reading non-interactives
			i = -1										#reset i=-1		
			while True:
				line = file_red.readline()
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

	file_red.close()

	print 
	print 'before randomzing sentences:'
	print 'number of interactive protein pairs:', len(sen_i)
	print 'number of non-interactive protein pairs:', len(sen_ni)

	c = 0												#calculate c for validation, make sure sum is right
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

#####################################################################################################################################


#################### disrupt the order of pretein pairs and keep the order of sentences of each protein pair ########################

	random.shuffle(sen_i)								#randomize the interactive protein pairs, however, sentences belonged to every interactive protein pair not moved
	random.shuffle(sen_ni)								#randomize the non-interactive protein pairs, however, sentences belonged to every non-interactive protein pair not moved


	file_ran = open(path_O, 'w+')

	for i in range(len(sen_i)):							#write the randomized interactive protein pairs into file
		for j in range(len(sen_i[i])):
			file_ran.write(sen_i[i][j])
	file_ran.write('--------------------------------------dividing line for interactive and non-interactive proteinpairs----------------------------------------------\n')
	for i in range(len(sen_ni)):						#write the randomized non-interactive protein pairs into file
		for j in range(len(sen_ni[i])):
			file_ran.write(sen_ni[i][j])		

	file_ran.close()	

#####################################################################################################################################


########################## check for confirming number of interactive and non-interactive sentences #################################

	sen_i_ran = [[]]
	sen_ni_ran = [[]]

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
							sen_ni_ran.append([])			#if is not the first protein pair and meet ***, append a new element
						sen_ni_ran[i].append(line)			#put non-interactive protein pair into [[]]
					else:
						sen_ni_ran[i].append(line)			#put non-interactive sentence into [[]]
				else:
					break
			
		else:
			if '***' in line:
				i += 1
				if i != 0:
					sen_i_ran.append([])					#if is not the first protein pair and meet ***, append a new element
				sen_i_ran[i].append(line)					#put interactive protein pair into [[]]
			else:
				sen_i_ran[i].append(line)					#if not ***, put into interactives

		if not line:
			break
	file_ch.close()		

	print 'after randomizing sentences:'
	print 'number of interactive protein pairs:', len(sen_i_ran)
	print 'number of non-interactive protein pairs:', len(sen_ni_ran)

	c = 0												#calculate c for validation
	for i in sen_i_ran:
		#print len(i)
		c += len(i)
	for i in sen_ni_ran:
		#print len(i)
		c += len(i)
	print 'number of all sentences:', c

	print 'number of all interactive sentences:', reduce(lambda x,y: x + y, map(lambda x: len(x)-1, sen_i_ran))
	print 'number of all non-interactice sentences', reduce(lambda x,y: x + y, map(lambda x: len(x)-1, sen_ni_ran))
	print 
	
#####################################################################################################################################



if __name__=="__main__":
	print 'debugging'		




