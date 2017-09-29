import smtplib
import sqlite3
import urllib.request as ur

import bs4
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

fromaddr = "sparshbbhs@gmail.com"
toaddr = "skkumarsparsh@gmail.com"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "News Articles"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "thisisanewpassword")

body = "\r\nHere are the news articles:\r\n\r\n\r\n"

quote_page = 'http://www.androidpolice.com/'
s = ur.urlopen(quote_page).read()
soup = bs4.BeautifulSoup(s, 'html.parser')
time_box = soup.find_all('time', attrs={'class': 'timeago-hover'})
name_box = soup.find_all('h2')
name = []
time = []
link = []

for i in range(0, len(name_box)):
    if name_box[i].a:
        name.append(name_box[i].text.strip().replace("'", ""))
        link.append(name_box[i].a.get('href'))
        time.append(time_box[i].text.strip())

quote_page2 = 'https://www.theverge.com/'
s2 = ur.urlopen(quote_page2).read()
soup2 = bs4.BeautifulSoup(s2, 'html.parser')
name_box2 = soup2.find_all('div', attrs={'class': 'c-entry-box--compact__body'})
name2 = []
link2 = []
time2 = []

for j in range(0, 10):
    name2.append(name_box2[j].h2.a.text.strip().replace("'", ""))
    link2.append(name_box2[j].h2.a.get('href'))
    if name_box2[j].div.time:
        time2.append(name_box2[j].div.time.text.strip())
    else:
        time2.append('No Date Specified')

conn = sqlite3.connect('news_articles.db')
c = conn.cursor()
c.execute('CREATE table if not exists newsarticles(article varchar(250), url varchar(500), date varchar(20), '
          'website varchar(20))')

body = body + "Android Police-\r\n\r\n"

for k in range(0, len(name)):
    c.execute("INSERT into newsarticles values('" + str(name[k]) + "','" + str(link[k]) + "','"
              + str(time[k]) + "','" + str('Android Police') + "')")
    body = body + str(name[k]) + ": " + str(link[k]) + "\r\n\r\n"

body = body + "\r\n\r\n\r\n"

body = body + "The Verge-\r\n\r\n"

for k in range(0, len(name)):
    c.execute("INSERT into newsarticles values('" + str(name2[k]) + "','" + str(link2[k]) + "','"
              + str(time2[k]) + "','" + str('The Verge') + "')")
    body = body + str(name2[k]) + ": " + str(link2[k]) + "\r\n\r\n"

conn.commit()
print(pd.read_sql_query('SELECT * FROM newsarticles', conn))
conn.close()

msg.attach(MIMEText(body, 'plain'))
text = msg.as_string().encode('utf-8')

server.sendmail(fromaddr, toaddr, text)
server.quit()
