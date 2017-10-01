import cx_Freeze
import sys
import smtplib
import urllib
import bs4

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("Project.py", base=base, icon="clienticon.ico")]

cx_Freeze.setup(
    name = "News WebScraper",
    options = {"build_exe": {"packages":["tkinter","bs4","smtplib","urllib","email.mime","datetime","sqlite3",], "include_files":["clienticon.ico"]}},
    version = "1.00",
    description = "Scrapes the websites specified for news articles",
    executables = executables
    )
