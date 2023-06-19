import time
import requests
import sqlite3
import os
conn = sqlite3.connect("radio.db")
c = conn.cursor()
while True:
    name = ""
    path = "C:/Users/Pofud/Desktop"
    try:
        os.chdir(path)
        print("Current working directory: {0}".format(os.getcwd()))
    except FileNotFoundError:
        pass
    t = time.localtime()
    out = ("%d-%d-%d-%d-%d-%d.mp3" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
    print(out)
    name = out
    time.sleep(3)
    stream_url = "http://46.20.7.116/babaradyoaac"
    c.execute("INSERT INTO radio(file_name,path) VALUES(?,?)",(name,path))
    r = requests.get(stream_url, stream=True)
    with open(out,"wb") as f:
        for block in r.iter_content(10000):
             f.write(block)
             break
    conn.commit()
