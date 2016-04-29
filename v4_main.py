import os
import requests
import sqlite3

name=raw_input('name?\n')
db_name=name+'.sqlite'

conn=sqlite3.connect(db_name)                        #database file
cur=conn.cursor()

# cur.execute('''
# CREATE TABLE IF NOT EXISTS Urls_Done (num NUMBER, url TEXT)''')

# cur.execute('''
# SELECT COUNT(url) FROM Urls_Done''')

# count=cur.fetchone()[0]+1
count = 1
cur.execute('''
SELECT url FROM Urls_To_Do WHERE (num>=? and num<?)''',(count,count+300))

urls=[el[0] for el in cur.fetchall()]

directory=name+'/'
if not os.path.exists(directory):
    os.makedirs(directory)

for url in urls:
    h=requests.head(url)
    print 'got head'
    if 20000<int(h.headers['content-length'])<5000000: 
    	print str(int(h.headers['content-length'])/1000)+" kb"           #making sure the file isn't a gif by making a rough estimate that the
        r=requests.get(url)                                 #content length is less than 1 MB
        type=url.split('.')[-1]
        print type
        f_name=os.path.join(directory, name+'_'+str(count)+'.'+type)
        with open(f_name,'wb') as f:
            f.write(r.content)
            f.close()
        print str(count)+" ------> "+str(url)
        # cur.execute('''
        # INSERT INTO Urls_Done (num,url) VALUES (?,?)''',(count,url))
        # conn.commit()
    else:
        print 'no good'
        # cur.execute('''
        # INSERT INTO Urls_Done (num,url) VALUES (?,?)''',(count,'no good'))
        # conn.commit()
    count+=1
conn.commit()