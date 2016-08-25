import i as search1
import datetime
import MySQLdb
db1 = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="LabBasedProject",charset='utf8' )
cursor1=db1.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS result (
	  ID INT(11) NOT NULL AUTO_INCREMENT,
	  Entity VARCHAR(100) ,
	  Occur date,
	  Nouns VARCHAR(1600),
	  WikiPageCreation date,
	  WikiEdit date,
	  NoOfEdits INT(10),
	  PRIMARY KEY (ID)
	) ENGINE=InnoDB
	""")

date=datetime.date(2016,01,01)
timeD=datetime.timedelta(1)

HashTable_entity={}
HashTable_nouns={}
for i in range(0,90):
	current_date=str(date+i*timeD)
	temp=search1.deciding_new_entity(current_date)
 	for key,value in temp.iteritems():
	 	if(HashTable_entity.has_key(key)):
	 		HashTable_nouns[key]=HashTable_nouns[key].union(value)
	 	else:
	 		HashTable_entity[key]=current_date
	 		HashTable_nouns[key]=value

	print current_date

print 'begining insertion'

for key,value in HashTable_entity.iteritems():
	nouns_set=HashTable_nouns[key]
	s=""
	for nouns in nouns_set:
		s+=nouns
		s+=" "
	s=s[0:len(s)-1]
	cursor1.execute("INSERT INTO `result` (`Entity`,`Occur`,`Nouns`) VALUES (%s,%s,%s)",(key,value,s))

db1.commit()

