import requests
from bs4 import BeautifulSoup
import sqlite3

conn=sqlite3.connect('candice.sqlite')                        #database file
cur=conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Urls (url TEXT)''')                

cur.execute('''
SELECT url FROM URLS''')

l=[r[0].encode() for r in cur.fetchall()]

count=len(l) + 1                                              #new batch starts where the last one ended

url='http://imgur.com/r/candiceswanepoel'

r= requests.get(url)

soup=BeautifulSoup(r.text,'html.parser')                     #html parser
posts=soup.find_all('a','image-list-link')                   #html tag of each image

'''The above method returns only 60 images since the rest of the page is Javascript rendered.
Noob method to download all images:
Load the imgur page. Open developer tools and copy the contents of each div element whose class is 'posts sub-gallery br5'.
Save all this content to a text file in the same folder as the Python file. Comment the previous 3 lines and uncomment the next 
4 lines. I'm gonna automate this step soon.'''

'''f=open('candice_html.txt')
soup=BeautifulSoup(f.read(),'html.parser')
f.close()
posts=posts=soup.find_all('a','image-list-link')
'''

for post in posts[:50]:
    src=post.find('img')['src']
    u=src[2:]
    url='http://'+str(u[:-5])+'.jpg'                        #retrieving the url of the full sized file from the url of the thumbnail
    if not url in l:
        r=requests.get(url)
        f_name='candice_'+str(count)+'.jpg'
        with open(f_name,'wb') as f:
                f.write(r.content)
                f.close()
        cur.execute ('INSERT INTO Urls (url) VALUES (?)',(url,))
        conn.commit()
        print count
        count+=1
    else:
        print 'Photo already downloaded'
