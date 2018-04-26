def divide_parts(path_I, n):
	print 
	print '-----------------------------------------------------------'
	print 'start dividing into parts of cross validation for testing...'

	sen_i = [[]]										#store interactive protein pairs and their sentences
	sen_ni = [[]]										#sotre non-interactice protein pairs and their sentences

############## read from text after reducing and randomizing sentences and store protein pairs and their senteces ##################

	file_r = open(path_I, 'r')

	i = -1												#set i=-1 for the first iteracion
	#for j in range(3):
	while True:
		line = file_r.readline()
		if '-----------------' in line:					#if meet ---- in line, convert into reading non-interactives
			i = -1										#reset i=-1	to satisfy the iteration
			while True:
				line = file_r.readline()
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

	file_r.close()

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


############## divide protein pairs into several parts and try to make number of sentences of each part balanced # ##################

	pos_dlist = []										#store the numbers of nodes that divide interactive protein pairs into several parts
	neg_dlist = []										#store the numbers of nodes that divide non-interactive protein pairs into several parts
	for i in range(n):
		pos_dlist.append(i * len(sen_i) / n)			#calculate the numbers of nodes and append into list
	pos_dlist.append(len(sen_i))						#add (the number of last protein pair) +1 into list 
	for i in range(n):
		neg_dlist.append(i * len(sen_ni) / n)			#calculate the numbers of nodes and append into list
	neg_dlist.append(len(sen_ni))						#add (the number of last protein pair) +1 into list 
		
	pos_fname = []										#store the names of n files of signatures
	neg_fname = []										#store the names of n files of signatures, the same as pos_fname
	name_before = "True label true pattern sentences_red_ran_"
	name_after = ".txt"
	for i in range(n):
		name = name_before + str(i) + name_after
		pos_fname.append(name)
	for i in range(n):
		name = name_before + str(i) + name_after
		neg_fname.append(name)

	print 'interactive protein pairs of each part:', pos_dlist
	print 'non-interactive protein pairs of each part:', neg_dlist
	print 
	print 'file name of each divided part:', pos_fname
	print 'file name of each divided part:', neg_fname
	print 



	c_i = []											#store the sum of interactive sentences(including protein pairs) of every part of signature
	c_ni = []											#store the sum of non-interactive sentences(including protein pairs) of every part of signature
	for m in range(n):
		c = 0
		for i in range(pos_dlist[m], pos_dlist[m+1]):
			c += len(sen_i[i])							#calculate the sum by adding the number of sentences of every interactive protein pair
		c_i.append(c)									#add the sum into interactive list

		c = 0
		for i in range(neg_dlist[m], neg_dlist[m+1]):
			c += len(sen_ni[i])							#calculate the sum by adding the number of sentences of every non-interactive protein pair
		c_ni.append(c)									#add the sum into non-interactive list


	for i in range(n):
		print 'totality of sentences and protein pairs of part '+str(i)+':', c_i[i]+c_ni[i]
	print 


	for i in range(len(c_i)):
		print 'number of interactive sentences of part'+str(i)+':', c_i[i] - (pos_dlist[i+1] - pos_dlist[i])
														#calculate the sum of sentences(not including protein pair) of all interactive protein pairs
	print

	for i in range(len(c_ni)):
		print 'number of non-interactive sentences of part'+str(i)+':', c_ni[i] - (neg_dlist[i+1] - neg_dlist[i])
														#calculate the sum of sentences(not including protein pair) of all interactive protein pairs
	print

	num_all = 0											#store the sum of all(interactives and non-interactives), add dependently
	num_plus = 0										#store the sum of all(interactives and non-interactives), add rely on every num(below)
	for m in range(n):
		path_O = pos_fname[m]
		fout = open(path_O, 'w+')
		num = 0											#reset num=0 for every iteraction
		for i in range(pos_dlist[m], pos_dlist[m+1]):
			for j in range(len(sen_i[i])):
				fout.write(sen_i[i][j])					#write every part of interactives into file
				num += 1								#count the sum of every interactive 
				num_all += 1							#count the sum of all interactives
#		print num,
		num_plus += num									#count the sum of every part of interactives

		fout.write("-------------------------------------- dividing line for interactive and non-interactive protein pairs ----------------------------------------------\n")

		num = 0
		for i in range(neg_dlist[m], neg_dlist[m+1]):
			for j in range(len(sen_ni[i])):
				fout.write(sen_ni[i][j])				#write every part of non-interactives into file
				num += 1								#count the sum of every interactive 
				num_all += 1							#count the sum of all interactives
#		print num,
		num_plus += num									#count the sum of every part of interactives

		fout.close()		

#	print
#	print '---------------------------'
#	print num_plus
#	print num_all
#	print '---------------------------'

	return pos_fname

if __name__=="__main__":
	print 'debugging'
