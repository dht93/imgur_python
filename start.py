<<<<<<< HEAD
import sqlite3
from bs4 import BeautifulSoup

print '\n\nCAUTION!! This is START'
print '-----------------------'
print ''
print ''
name=raw_input('name?\n')

db_name=name + '.sqlite'

conn=sqlite3.connect(db_name)                        #database file
cur=conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Urls_To_Do (num NUMBER KEY, url TEXT)''')

f_name=name + '.txt'

f=open(f_name)
soup=BeautifulSoup(f.read(),'html.parser')
f.close()

posts=soup.find_all('a','image-list-link')

count=1
print str(len(posts))+ ' entries'
for post in posts:
    src=post.find('img')['src']
    u=src[2:]
    type=post.next_sibling.next_sibling.contents[3].contents[0].strip().split(' ')[0].strip()
    if type=='image':
    	url='http://'+str(u[:-5])+'.jpg'
    else:
    	url='http://'+str(u[:-5])+'.gif'
    # print url
    cur.execute('''
    INSERT INTO Urls_To_Do (num,url) VALUES (?,?)''',(count, url))
    # conn.commit()
    count+=1
conn.commit()
print 'done'
=======
'''This is the first step of the process. A request to the Imgur page returns only 60 images since the rest of the page is Javascript
rendered.
Noob way to get all the links:
Load the Imgur page in the browser. Open developer tools. Copy the entire div element that has class="imagelist".
Paste the content in a text file in the same folder as the python file.
I'll automate this step soon '''

import sqlite3
from bs4 import BeautifulSoup

name=raw_input('name?\n')                            #name of the text file minus the extension. This makes the code reusable for
db_name=name + '.sqlite'                             #different bunch of images

conn=sqlite3.connect(db_name)                        #database file
cur=conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Urls_To_Do (num NUMBER PRIMARY KEY, url TEXT)''')        #table to store urls to be downloaded

f_name=name + '.txt'

f=open(f_name)
soup=BeautifulSoup(f.read(),'html.parser')
f.close()

posts=soup.find_all('a','image-list-link')

count=1

for post in posts:
    src=post.find('img')['src']
    u=src[2:]
    url='http://'+str(u[:-5])+'.jpg'
    cur.execute('''
    INSERT INTO Urls_To_Do (num,url) VALUES (?,?)''',(count, url))
    conn.commit()
    count+=1
print 'done'
>>>>>>> dcf786e12e84916ac453d38fea90577ec526e013
