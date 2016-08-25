'''

This File Processes Data From TaggedTokens File
It creates a HashTable and makes sure (name,type) is unique

'''
readFile=open('TaggedTokens','r')
writeFile=open('TrainingData','w')

lines=readFile.read().split('\n')

rows=list()
for line in lines :
	if len(line.split())==3:
		rows.append(tuple(line.split()))

HashTable={}
for row in rows:
	if HashTable.has_key((row[0],row[1])):
		HashTable[(row[0],row[1])]=(int(HashTable[(row[0],row[1])])+int(row[2]))
	else :
		HashTable[(row[0],row[1])]=int(row[2])

for key,value in HashTable.iteritems() :
	writeFile.write("%s\t%s\t%s\n" %(key[0],key[1],value))

readFile.close()
writeFile.close()
