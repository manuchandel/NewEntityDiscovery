import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="LabBasedProject",charset='utf8' )
cursor=db.cursor()

cursor.execute("SELECT * FROM `Twitter_Names` WHERE 1")
indian_names=cursor.fetchall()

# unify Indian Names into tokens and count frequencies of each token
HashTable={}
for name in indian_names:
	name_list=name[1].split()
	for each_name in name_list:
		if len(each_name)>3:
			if HashTable.has_key(each_name.lower()):
				HashTable[each_name.lower()]=int(HashTable[each_name.lower()])+1
			else :
				HashTable[each_name.lower()]=1

writeFile=open('Indian_Twitter_Name_Token','w')

for key,value in HashTable.iteritems() :
		writeFile.write("%s\t%s\t%d\n" %(key,'PERSON',int(value)))
cursor.close()
