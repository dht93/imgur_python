'''This is the first step of the process. A request to the Imgur page returns only 60 images since the rest of the page is Javascript
rendered.
Noob way to get all the links:
Load the Imgur page in the browser. Open developer tools. Copy the entire div element that has class="imagelist".
Paste the content in a text file in the same folder as the python file.
I'll automate this step soon '''

import sqlite3
from bs4 import BeautifulSoup

conn=sqlite3.connect('candice.sqlite')                        #database file
cur=conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Urls_To_Do (num NUMBER, url TEXT)''')

f=open('candice.txt')
soup=BeautifulSoup(f.read(),'html.parser')
f.close()

posts=soup.find_all('a','image-list-link')

count=1

for post in posts:
    src=post.find('img')['src']
    u=src[2:]
    url='http://'+str(u[:-5])+'.jpg'
    cur.execute('''
    INSERT INTO Urls_To_Do (num,url) VALUES (?,?)''',(count, url))      #inserting the urls to be downloaded into a new table
    conn.commit()
    count+=1
print 'done'
