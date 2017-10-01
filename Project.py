import smtplib
import sqlite3
import urllib.request as ur
import tkinter as tk
from tkinter import ttk
from datetime import datetime

import bs4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

LARGE_FONT = ("Verdana", 12)

conn = sqlite3.connect('email.db')
c = conn.cursor()

c.execute('CREATE table if not exists email(e varchar(50))')

c.execute("SELECT e from email")
data = c.fetchone()
print(data)
if data is None:
    toaddr = "skkumarsparsh@gmail.com"
    c.execute("INSERT into email values('" + toaddr + "')")
else:
    toaddr = data[0]

conn.commit()
conn.close()

fromaddr = "sparshbbhs@gmail.com"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr


class FirstApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "News Web Scraper")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.update()
        frame.event_generate("<<ShowFrame>>")


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Welcome to the WebScraper Application", font=LARGE_FONT)
        label.pack(pady=50, padx=50)

        button = ttk.Button(self, text="Retrieve News Articles", command=lambda: controller.show_frame(PageOne))
        button.pack(pady=10, padx=20)

        button = ttk.Button(self, text="Change Email Address", command=lambda: controller.show_frame(PageThree))
        button.pack(pady=10, padx=20)

        button2 = ttk.Button(self, text="See the News Articles Archive", command=lambda: controller.show_frame(PageTwo))
        button2.pack(pady=10, padx=20)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = ttk.Label(self, text="Please wait while the news articles are collected and sent to your email..."
                               , font=LARGE_FONT)
        self.label.pack(pady=50, padx=50)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10, padx=20)

        self.bind("<<ShowFrame>>", self.onShowFrame)

    def reset(self):
        self.label.configure(text="Please wait while the news articles are collected and sent to your email...")

    def onShowFrame(self, event):
        self.reset()
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "thisisanewpassword")
            msg['Subject'] = "News Articles - " + str(datetime.now())

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
            c.execute(
                'CREATE table if not exists newsarticles(article varchar(250), url varchar(500), date varchar(20), '
                'website varchar(20))')

            body = body + "Android Police-\r\n\r\n"

            for k in range(0, len(name)):
                c.execute("SELECT * from newsarticles where article = ?", (name[k],))
                data = c.fetchone()
                if data is None:
                    c.execute("INSERT into newsarticles values('" + str(name[k]) + "','" + str(link[k]) + "','"
                              + str(time[k]) + "','" + str('Android Police') + "')")
                body = body + str(name[k]) + ": " + str(link[k]) + "\r\n\r\n"

            body = body + "\r\n\r\n\r\n"
            body = body + "The Verge-\r\n\r\n"

            for k in range(0, len(name)):
                c.execute("SELECT * from newsarticles where article = ?", (name2[k],))
                data = c.fetchone()
                if data is None:
                    c.execute("INSERT into newsarticles values('" + str(name2[k]) + "','" + str(link2[k]) + "','"
                              + str(time2[k]) + "','" + str('The Verge') + "')")
                body = body + str(name2[k]) + ": " + str(link2[k]) + "\r\n\r\n"

            conn.commit()

            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string().encode('utf-8')

            server.sendmail(fromaddr, toaddr, text)
            conn.close()
            server.quit()

            self.label.config(text="News articles emailed successfully:)")
        except:
            self.label.config(text="Oops some error occurred:(")


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Archive of the News Articles", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.bind("<<ShowFrame>>", self.onShowFrame)

        self.tree = ttk.Treeview(self, columns=('URL', 'Time', 'Website'))
        self.tree.column('#0', width=550)
        self.tree.column('URL', width=180)
        self.tree.column('Time', width=180)
        self.tree.column('Website', width=120)
        self.tree.heading('#0', text='Article')
        self.tree.heading('URL', text='URL')
        self.tree.heading('Time', text='Time')
        self.tree.heading('Website', text='Website')
        self.tree.pack(padx=10, pady=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10, padx=20)

    def onShowFrame(self, event):
        conn = sqlite3.connect('news_articles.db')
        c = conn.cursor()

        c.execute('SELECT article from newsarticles')
        articles = c.fetchall()

        c.execute('SELECT url from newsarticles')
        urls = c.fetchall()

        c.execute('SELECT date from newsarticles')
        dates = c.fetchall()

        c.execute('SELECT website from newsarticles')
        websites = c.fetchall()

        for i in range(0, len(articles)):
            self.tree.insert('', 'end', text=articles[i][0], values=(urls[i][0], dates[i][0], websites[i][0]))

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = ttk.Label(self, text="The current email address for sending news articles is " + toaddr, font=LARGE_FONT)
        self.label.pack(pady=50, padx=50)

        label2 = ttk.Label(self, text="Enter the new email address:", font=LARGE_FONT)
        label2.pack(pady=1)

        self.entry = ttk.Entry(self, width=50)
        self.entry.pack(padx=10, pady=10)

        button = ttk.Button(self, text="Change Email Address", command=self.changeEmail)
        button.pack(pady=10, padx=20)

        button2 = ttk.Button(self, text="Go back", command=lambda: controller.show_frame(StartPage))
        button2.pack(pady=10, padx=20)

    def changeEmail(self):
        global toaddr
        toaddr = self.entry.get()
        self.label.configure(text="The current email address for sending news articles is " + toaddr)

        conn = sqlite3.connect('email.db')
        c = conn.cursor()
        c.execute("DROP table email")
        c.execute('CREATE table email(e varchar(50))')
        c.execute("INSERT into email values('" + toaddr + "')")
        conn.commit()
        conn.close()

app = FirstApp()
app.mainloop()
