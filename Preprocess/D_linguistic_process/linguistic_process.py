import string
import nltk
#import enchant
import os
import re
#from nltk.tag.stanford import StanfordPOSTagger
from nltk.parse.stanford import StanfordParser
#from nltk.parse.stanford import StanfordDependencyParser

class linguistic_process:

	def __init__(self, division_parts):
		self.division_parts = division_parts

	def WordTokener(self, line):
		#print 'start wordtokenize'
		word = nltk.word_tokenize(line)		#word tokenize using ntlk
		line = ' '.join(word)				#re-form sentences using words after word tokenize
		return line

	def CleanLines(self, line):
		#print 'start clean lines(remove punctuation)'
		table = string.maketrans('!"$%&\'()*+,-./:;<=>?@[\\]^_`{|}~','                               ')		#character mapping conversion table
		line = line.translate(table)				#replace punctuation except # with space
		return line

	"""def WordCheck(self, line):
		#print 'start wordcheck'
		word = line.split()					#split line by space
		d = enchant.Dict("en_US")
		word = filter(lambda w: d.check(w), word)
		'''for w in word:					#remove in list like this may cause problems
			if not d.check(w):				#if w is appropriate, d.check(w) return True, else return False
				print w			
				word.remove(w)				#remove w from the word list'''
		line = ' '.join(word)				#re-form sentences using words after word check
		return line"""

	def CleanWords(self, line):
		#print 'start clean words(remove non-alpha and len<3 words)'
		matchOBJ = re.match(r'(.*)#(.*)#(.*)#(.*)#(.*)',line,re.I)
		line_dirty = []
		if matchOBJ:
			e1 = matchOBJ.group(2)
			e2 = matchOBJ.group(4)
			line_dirty.append(matchOBJ.group(1))
			line_dirty.append(matchOBJ.group(3))
			line_dirty.append(matchOBJ.group(5))
		
		line_clean = []
		for l_dirty in line_dirty:
			word = l_dirty.split()			#split line by space
			#cleanwords = [w.lower() for w in word if 3<=len(w) and w.isalpha()]	#remove words that is non-alpha and len(word)<3 and translate words to lower
			cleanwords = filter(lambda w: len(w)>1 and w.isalnum() and not w.isdigit(), word)			#remove words that is non-alpha and len(word)<3
			
			cleanwords = map(lambda w: w.lower(), cleanwords)						#translate words to lower
			l_clean = ' '.join(cleanwords)											#re-form sentences using words after clean words
			line_clean.append(l_clean)
			
		line_split = []
		line_split.append(line_clean[0])
		line_split.append('#'+e1+'#')
		line_split.append(line_clean[1])
		line_split.append('#'+e2+'#' )
		line_split.append(line_clean[2])
		line = ' '.join(line_split)
		#print line
		return line

	def CleanStopWords(self, line):
		#print "start clean stopwords"
		word = line.split()										#split line by space
		stopwords = nltk.corpus.stopwords.words("english")
		word = map(lambda w: w.lower(), word)					#translate words to lower
		word = filter(lambda w: w not in stopwords, word)		#remove the stopwords
		line = ' '.join(word)									#re-form sentences using words after removing stopwords
		return line

	"""def POSTag(self, line):
		#print 'start POSTagging...'	
		st = StanfordPOSTagger('english-bidirectional-distsim.tagger')			#nltk interfaces StanfordPOSTagger
		tag_t = st.tag(line.split())								#tage_t is a list that contain tuple as element
		print tag_t		
		tag_s = map(lambda x: '|'.join(x), tag_t)					#join element in tuple by |
		#print tag_s
		line = ' '.join(tag_s)										#join element in list by space
		return line

	def Parser(self, line):
		#print 'start parsering...'
		parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")			#nltk interfaces StanfordParser
		print list(parser.raw_parse(line))	"""						#return the parsered result as a list

	def unigram(self, path_div):
		print 
		print '-----------------------------------------------------------'
		print 'start unigram processing...'

		i = 0
		for division_part in self.division_parts:					#cyclic process every division part, division_part in division_parts is the path 
			fin = open(division_part, 'r')							#open the input file along the path
			fout = open(path_div+'/'+os.path.split(path_div)[1]+'_'+str(i)+'.txt', 'w+')		#open the output file along the path including the directory and the file name(first part is the same as the directory and second part is _ and number)
			i += 1
		
			#for j in range(3):
			while True:
				line = fin.readline()
				if line:
					if '***' in line:
						fout.write(line)							#write protein pair into file 
					elif '--------------------' in line:
						fout.write(line)							#write dividing line into file
					else:
						line = self.WordTokener(line)				#first, wordtokenization
						line = self.CleanLines(line)				#second clean line, e.g. remove punctuation except |
						line = self.CleanStopWords(line)			#last, clean stopwords
						line = self.CleanWords(line)
						fout.write(line + '\n')						#after processing, write into file
				else:
					break

			fin.close()
			fout.close()

	def unigram_POSTag(self, path_div):
		print 
		print '-----------------------------------------------------------'
		print 'start unigram_postag processing...'

		i = 0
		for division_part in self.division_parts:					#cyclic process every division part, division_part in division_parts is the path
			fin = open(division_part, 'r')
			fout = open(path_div+'/'+os.path.split(path_div)[1]+'_'+str(i)+'.txt', 'w+')			#open the output file along the path including the directory and the file name(first part is the same as the directory and second part is _ and number)
			i += 1
			
			for j in range(3):
			#while True:
				line = fin.readline()								#write protein pair into file 
				if line:
					if '***' in line:
						fout.write(line)							#write dividing line into file
					elif '--------------------' in line:
						fout.write(line)
					else:
						line = self.WordTokener(line)				#first, wordtokenization
						line = self.POSTag(line)					#second, part of speech tagging
						fout.write(line + '\n')						#finally, write into file
				else:
					break

			fin.close()
			fout.close()

if __name__=="__main__":
	print 'debugging'
