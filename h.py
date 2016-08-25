import MySQLdb
db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="LabBasedProject",charset='utf8' )
cursor=db.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS HeadLines (
	  ID INT(11) NOT NULL AUTO_INCREMENT,
	  NEWS VARCHAR(1600) ,
	  DATE date,
	  SOURCE VARCHAR(100),
	  PRIMARY KEY (ID)
	) ENGINE=InnoDB
	""")

cursor.execute("SELECT * FROM `local_information_repository` WHERE 1")
url_list=cursor.fetchall()

print "Read Data"

def extract_source(S):
	i=S.find(".com");
	if i==-1 :
		return ''
	source='';
	i=i-1
	while ord(S[i])>=97 and ord(S[i])<=122:
		source+=S[i]
		i-=1
	return source[::-1]
#extract source all names
for row in url_list:
	url=row[7];
	source=extract_source(url)
	if len(source)>0:
		cursor.execute("INSERT INTO `HeadLines` (`NEWS`,`DATE`,`SOURCE`) VALUES (%s,%s,%s)",(row[1],row[2],source))
		
db.commit()
