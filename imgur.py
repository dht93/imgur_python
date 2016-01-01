'''Once the database of urls is built using start.py, use this code to download the images'''

import requests
import sqlite3

conn=sqlite3.connect('candice.sqlite')                        #database file
cur=conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Urls_Done (num NUMBER, url TEXT)''')

cur.execute('''
SELECT COUNT(url) FROM Urls_Done''')

count=cur.fetchone()[0]+1

cur.execute('''
SELECT url FROM Urls_To_Do WHERE (num>=? and num<?)''',(count,count+10))

urls=[el[0] for el in cur.fetchall()]

for url in urls:
    h=requests.head(url)
    if int(h.headers['content-length'])<1000000:            #making sure the file isn't a gif by making a rough estimate that the
        r=requests.get(url)                                 #content length is less than 1 MB
        f_name='candice_'+str(count)+'.jpg'
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
