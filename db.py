import os
import sqlite3

conn = None
if os.path.exists("./pta.sqlite"): # creating sql database
    conn = sqlite3.connect('pta.sqlite')
else:
    sqlite3.connect('pta.sqlite')   # creating sql database
    conn = sqlite3.connect("./pta.sqlite")
    c = conn.cursor()
    c.execute("CREATE TABLE 'project' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"\
        "'name'  TEXT NOT NULL UNIQUE, "\
        "'hosts' TEXT, "\
        "'ports' TEXT, "\
        "'prots' TEXT, "\
        "'http_s');")
    c.execute("CREATE TABLE 'r_nmap' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"\
        "'pid'  INTEGER, "\
        "'datetime'  TEXT, "\
        "'host'  TEXT, "\
        "'hostname'  TEXT, "\
        "'hostname_type'  TEXT, "\
        "'protocol' TEXT, "\
        "'port' TEXT, "\
        "'name' TEXT,"\
        "'state' TEXT,"\
        "'product' TEXT,"\
        "'extrainfo' TEXT,"\
        "'reason' TEXT,"\
        "'version' TEXT,"\
        "'conf' TEXT,"\
        "'cpe' TEXT,"\
        "'status' INTEGER DEFAULT 0);")
    conn.commit()