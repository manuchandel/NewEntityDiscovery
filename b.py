import MySQLdb
import nltk
import re
from nltk.tag import StanfordNERTagger
db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="LabBasedProject",charset='utf8' )
cursor=db.cursor()
st = StanfordNERTagger('/home/ubuntu/LabBasedProject/stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz','/home/ubuntu/LabBasedProject/stanford-ner-2014-08-27/stanford-ner.jar')

# select 800k headlines from `HeadLine`
cursor.execute("SELECT `newsHeadline` FROM `local_information_repository` ORDER By `ID`")
headlines=cursor.fetchall()

# for each 50k headlines write tokens into text files namely  text0, text1.....text15
for i in range(0,800000):
	if i % 50000 == 0:
		f = open('Tokens/text%d' % int(i/50000), 'w')
	tokens=nltk.tokenize.word_tokenize(headlines[i][0])
	for token in tokens:
		s=re.sub('[^A-Za-z0-9]+', '',token)
		if len(s)>0 :
			f.write(s)
			f.write('\n')

cursor.close()
