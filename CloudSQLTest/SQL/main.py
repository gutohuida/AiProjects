import MySQLdb

myDB = MySQLdb.connect(host="35.235.12.109",port=3306,user="root",passwd="gbg@544632",db="gbg")
cHandler = myDB.cursor()
cHandler.execute("SELECT * from evento")
results = cHandler.fetchall()
for items in results:
    print(items)