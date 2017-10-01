import cx_Freeze
import sys
import smtplib
import urllib
import bs4
import os
import tkinter

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = "C:\\Users\\spars\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\spars\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

executables = [cx_Freeze.Executable("Project.py", base=base, icon="clienticon.ico")]

cx_Freeze.setup(
    name = "News WebScraper",
    options = {"build_exe": {"packages":["tkinter","bs4","smtplib","urllib","email.mime","datetime","sqlite3",], "include_files":["clienticon.ico", "tcl86t.dll", "tk86t.dll"]}},
    version = "1.00",
    description = "Scrapes the websites specified for news articles",
    executables = executables
    )
