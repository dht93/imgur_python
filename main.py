'''Once the database of urls is built using start.py, use this code to download the images'''

import os
import requests
import sqlite3

name=raw_input('name?\n')                           #for re-usability
db_name=name+'.sqlite'

conn=sqlite3.connect(db_name)                        #database file
cur=conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Urls_Done (num NUMBER, url TEXT)''')

cur.execute('''
SELECT COUNT(url) FROM Urls_Done''')

count=cur.fetchone()[0]+1

cur.execute('''
SELECT url FROM Urls_To_Do WHERE (num>=? and num<?)''',(count,count+10))

urls=[el[0] for el in cur.fetchall()]

directory='D:/Code/PY/Imgur/'+name+'/'                     
if not os.path.exists(directory):
    os.makedirs(directory)

for url in urls:
    h=requests.head(url)
    if 20000<int(h.headers['content-length'])<1000000:      #making sure the file isn't a gif by making a rough estimate that the
        r=requests.get(url)                                 #content length is less than 1 MB. Also discarding images less than 20KB
        f_name=os.path.join(directory, name+'_'+str(count)+'.jpg')
        with open(f_name,'wb') as f:
            f.write(r.content)
            f.close()
        print url
        cur.execute('''
        INSERT INTO Urls_Done (num,url) VALUES (?,?)''',(count,url))
        conn.commit()
    else:
        print 'gif'
        cur.execute('''
        INSERT INTO Urls_Done (num,url) VALUES (?,?)''',(count,'gif'))
        conn.commit()
    count+=1

