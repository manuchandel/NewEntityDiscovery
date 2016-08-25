import nltk
from nltk.tag import StanfordNERTagger
st = StanfordNERTagger('/home/ubuntu/LabBasedProject/stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz','/home/ubuntu/LabBasedProject/stanford-ner-2014-08-27/stanford-ner.jar')

#writeFile where taggedtokens will written
writeFile=open('Tagged_Tokens','w')

for i in range(0,16):

	#open a file with tokens
	f=open('Tokens/text%d' % i,'r')
	tokens=f.read().split()


	# print 'Tokens read from file %d' % i
	ner_tokens=st.tag(tokens)
	
	# print 'Tokens Tagged'

	HashTable={}

	# make sure tokens in this file are unique
	for token in ner_tokens :
		if HashTable.has_key((token[0].lower(),token[1])):
			HashTable[(token[0].lower(),token[1])]+=1
		else :
			HashTable[(token[0].lower(),token[1])]=1
		
	# print 'write into the file'
	for key,value in HashTable.iteritems() :
		writeFile.write("%s\t%s\t%d\n" %(key[0],key[1],value))

	f.close()

writeFile.close()