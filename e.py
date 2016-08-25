import MySQLdb
db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="LabBasedProject",charset='utf8' )
cursor=db.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS TrainingDataDictionery (
  	TOKEN VARCHAR(20) NOT NULL,
  	TYPE VARCHAR(12) NOT NULL,
  	COUNT INT(10),
  	PRIMARY KEY (TOKEN, TYPE)
	) ENGINE=InnoDB
	""")

readFile=open('Training_Data','r')

lines=readFile.read().split('\n')

for line in lines:
	if len(line.split()) ==3 : 
		values=line.split()
		if len(values[0]) <=20:
			cursor.execute("INSERT INTO `TrainingDataDictionery` (`TOKEN`,`TYPE`,`COUNT`) VALUES (%s,%s,%s)", (values[0],values[1],int(values[2])))
db.commit()
cursor.close()
