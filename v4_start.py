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
