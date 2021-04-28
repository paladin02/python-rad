import os
import time
import requests
import sys
import psycopg2
list = ""
try:
	conn = psycopg2.connect("dbname='hasbel' user='paladin' password='123'")
	print("Connected")
except:
	print("No")	
try:
	conn1 = psycopg2.connect("dbname='deneme' user='paladin' password='123'");
	print("Connected")
except:
	print("no")
cursor = conn.cursor()
cursor2 = conn1.cursor()
try:
	cursor.execute("SELECT url FROM admin")
	rows = cursor.fetchall()
	for rows in rows:
		link = rows[0]
		print(link)
except:
	print("no")
path = "/home/paladin/Masaüstü/"
try:
    os.chdir(path)
    print("Current working directory: {0}".format(os.getcwd()))
except FileNotFoundError:
    pass
while True:
    t = time.localtime()
    out = ("%d-%d-%d-%d:%d:%d.mp3" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
    list = out
    print("Database Name : ",list) 
    print(out)
    time.sleep(3)
    cursor2.execute("INSERT INTO output(files,path) VALUES(%s,%s)",(list,path));
    r = requests.get(link, stream=True)
    with open(out,"wb") as f:
        for block in r.iter_content(57601968):
            f.write(block)
            break
    conn1.commit();
   
