import MySQLdb
import nltk
import datetime
db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="LabBasedProject",charset='utf8' )
cursor=db.cursor()

# Create Set of Person Names
cursor.execute("SELECT * FROM `TrainingDataDictionery` T1 WHERE `Type`='PERSON' and NOT EXISTS (SELECT * FROM `TrainingDataDictionery` WHERE `Token`=T1.Token and `COUNT`>T1.count) ")
rows=cursor.fetchall()
fetched_list=list()

for row in rows:
	fetched_list.append(row[0])

person_names=set(fetched_list)

# Create set of WikiHumans
cursor.execute("SELECT * FROM `WikiHumans` WHERE 1")
rows=cursor.fetchall()
fetched_list=[]

for row in rows:
	fetched_list.append(row[1])

wikiHumans_names=set(fetched_list)

print 'preprocessing completed'
# returns list of combined names
def list_of_combined_names(nltk_tagged_tokens,nltk_person_list):
	potential_entity_name=''
	potential_entity_list=list()
	for token in nltk_tagged_tokens:
		if token[1]=='NNP' and token[0].lower() in nltk_person_list:
			potential_entity_name+=token[0]
			potential_entity_name+=' ' 
		else:
			if len(potential_entity_name)>0:
				potential_entity_list.append(potential_entity_name[0:len(potential_entity_name)-1])
				potential_entity_name=''

	if len(potential_entity_name)>0:
		potential_entity_list.append(potential_entity_name[0:len(potential_entity_name)-1])
		potential_entity_name=''

	return potential_entity_list

# checks whether entity is present in wikiHumans or not
def new_entity_set(potential_entity_list):
	new_entity_list=list()
	for entity in potential_entity_list:
		if len(entity.split())>1 and entity.lower() not in wikiHumans_names:
			new_entity_list.append(entity)

	return set(new_entity_list)

# returns new entities of all headlines of a given dates
def find_new_entity_set(date):

	new_entity=set()

	cursor.execute("SELECT * FROM `HeadLines` WHERE `DATE` = %s ",(date))
	rows=cursor.fetchall()


	for headline in rows:
		tokens=nltk.tokenize.word_tokenize(headline[1])
		nltk_tagged_tokens=nltk.pos_tag(tokens)
		potential_entity_list=list_of_combined_names(nltk_tagged_tokens,person_names)
		new_entity= new_entity.union(new_entity_set(potential_entity_list))

	return new_entity

# returns matrix of related nouns
def create_matrix(headlines, entity) :
	HashTable={}
	nouns_associated=list()
	sources=list()
	entity_noun=entity.lower().split()
	for headline in headlines:
		tokens=nltk.tokenize.word_tokenize(headline[1])
		nltk_tagged_tokens=nltk.pos_tag(tokens)
		for tagged_token in nltk_tagged_tokens:
			if (tagged_token[1]=='NNP' or tagged_token[1]=='JJ') and (tagged_token[0].lower() not in entity_noun):
				if HashTable.has_key(tagged_token[0]):
					HashTable[tagged_token[0]]+=1
				else :
					nouns_associated.append(tagged_token[0])
					HashTable[tagged_token[0]]=int(1)
		sources.append(headline[3])

	n=len(headlines)
	nouns_set=set(nouns_associated)
	for key,value in HashTable.iteritems():
		if value < int(n/2):
			nouns_set.remove(key)

	return (nouns_set,set(sources))

# returns entity list with related nouns discovered at particular date
def deciding_new_entity(date):
	dictionery={}
	new_entity=find_new_entity_set(date)
	return_string=""
	for entity in new_entity:
		cursor.execute("SELECT * FROM  `HeadLines` WHERE `NEWS` LIKE %s AND `DATE` =%s",('%'+entity+'%',date))
		occurences=cursor.fetchall()
		if len(occurences)>5:
			cursor.execute("SELECT * FROM  `HeadLines` WHERE `NEWS` LIKE %s AND `DATE` < DATE(DATE_SUB(%s,INTERVAL 5 DAY)) ",('%'+entity+'%',date))
			rows =cursor.fetchall()
			if len(rows)==0  :
				matrix=create_matrix(occurences,entity)
				if len(matrix[1])>=3:
					dictionery[entity.lower()]=matrix[0]

	return dictionery
