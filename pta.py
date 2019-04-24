import nmap
import sys
import os
import json
import sqlite3
import csv


# GLOBALS
conn = None
proj = None

def clrs():
    os.system('clear')

def p_logo():
    print("PTA - PenTestAutomatizer version 0.1 alpha\n") # to run:  python3 /root/Documents/pythonfolder/hello.py
    print("PPPPPP    TTTTTTTTT      A")
    print("PP  PPP   TTTTTTTTT     AAA")
    print("PP  PPP      TTT       AA AA")
    print("PPPPPP       TTT      AA   AA")
    print("PPP          TTT     AAAAAAAAA")
    print("PPP          TTT    AAAAAAAAAAA")
    print("PPP          TTT   AAAA     AAAA\n")

def create_p(name, hosts, ports, prots):
    global data
    #sqll_ins("project", [name, hosts, ports, prots])
    c = conn.cursor()
    c.execute("INSERT INTO project  VALUES (NULL, '" + name + "', '" + hosts + "', '" + ports + "', '" + prots + "')")
    conn.commit()

def load_proj(name):
    global proj
    c = conn.cursor()
    for row in c.execute("SELECT * FROM project WHERE name='" + name + "'"):
        #proj = [row['id'], row['name'], row['hosts'], row['ports'], row['prots']]
        proj = row


def sqll_ins(table, arr):
    global conn
    cmd = "INSERT INTO " + table + " VALUES (NULL, " + str(proj[0])
    for entr in arr:
        cmd = cmd + ", '" + entr + "'"
    cmd = cmd + ")"

    print(cmd)
    c = conn.cursor()
    c.execute(cmd)
    conn.commit()


def run_nmap():
    global proj
    print(proj)
    nm = nmap.PortScanner() # init
    nm.scan(hosts=proj[2], ports=proj[3])
    #sqll_ins("r_nmap", nm.csv().split(';', 0))

    #print(nm.csv())
    iternmcsv = iter(nm.csv().splitlines())
    next(iternmcsv)
    for row in iternmcsv:
        sqll_ins("r_nmap", row.split(';'))


def run_nikto(hostname, port):
    global proj
    os.system("nikto -Display V -o _tmp_nikto.csv -Format csv -Tuning 9 -h " + hostname)
    _file = open('_tmp_nikto.csv', 'r')

    reader = csv.reader(open('_tmp_nikto.csv', 'r'), delimiter=',')
    itercsv = iter(reader)
    next(itercsv)
    for row in itercsv:
        sqll_ins("r_nikto", row)

    # delete


# start
clrs()
p_logo()

if os.path.exists("./pta.sqlite"):
    print("DB exists")
    conn = sqlite3.connect('pta.sqlite')
else:
    sqlite3.connect('pta.sqlite')
    conn = sqlite3.connect("./pta.sqlite")
    c = conn.cursor()
    c.execute("CREATE TABLE 'project' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"\
        "'name'  TEXT NOT NULL UNIQUE, "\
        "'hosts' TEXT, "\
        "'ports' TEXT, "\
        "'prots' TEXT);")
    c.execute("CREATE TABLE 'r_nmap' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"\
        "'pid'  INTEGER, "\
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
        "'cpe'  TEXT);")
    c.execute("CREATE TABLE 'r_nikto' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"\
        "'pid'  INTEGER, "\
        "'2'  TEXT, "\
        "'3' TEXT, "\
        "'4' TEXT, "\
        "'5' TEXT,"\
        "'6' TEXT, "\
        "'7' TEXT, "\
        "'8' TEXT);")
    conn.commit()


print("Menu:")
print("0     : exit programm")
print("1     : create project")
print("2     : load project")
print("3     : delete project")

i_nr=input()
######################################################################
if i_nr == "0":
    sys.exit()
######################################################################
elif i_nr == "1":
    clrs()
    p_logo()
    print("create project")
    i_proj  = input("project name: ")
    i_hosts = input("hosts (ip): ")
    i_prot  = input("TCP (0) or UDP (1) or BOTH (2): ")
    i_port  = input("ports : ")

    create_p(i_proj, i_hosts, i_port, i_prot)
######################################################################
elif i_nr == "2": # Funktion: Projekte laden
    clrs()
    p_logo()

    i=0
    c = conn.cursor()
    for row in c.execute("SELECT * FROM project ORDER BY id"):
        print("[" + str(i) + "] " + row[1])
        i = i + 1

    print("which project would you like to load?")
    i_proj  = input("proj: ")

    load_proj(i_proj)
    clrs()
    p_logo()

    print("actual project: " + proj[2])
    print("options: ")
    print("[0] scan all")
    print("[x] show report")
    print("[x] change modules")
    i_nr = input("option: ")

    if i_nr == "0":
        run_nikto("127.0.0.1", "80")
        #run_nmap()
        ###########

        ###########


######################################################################
elif i_nr == "3": # Funktion: Projekt löschen
    clrs()
    p_logo()
    print("which project would you like to delete?")

    i=0
    c = conn.cursor()
    for row in c.execute("SELECT * FROM project ORDER BY id"):
        print("[" + str(i) + "] " + row[1])
        i = i + 1

    i_nr = input("your input:") #löschendes projekt auswählen


    sql = "DELETE FROM project WHERE name='" + i_nr + "'"
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    print(i_nr + " was delete")
######################################################################

#"""erklärung für uns
#nmap -sS -sV -sC -Pn -n -vv -O -p1-65535 -oA nmapscan_full_tcp_$IP <ip | domain>
#-sS                 // TCP SYN
#-sV                 // Probe open ports to determine service/version info
#-sC                 // equivalent to --script=default
#--script=<yolo>     // <yolo> is a comma separated list of directories, script-files or script-categories
#-Pn                 // Treat all hosts as online -- skip host discovery
#-n                  // -n/-R: Never do DNS resolution/Always resolve [default: sometimes]
#-v                  // Increase verbosity level (use -vv or more for greater effect)
#-O                  // -O: Enable OS detection
#-p1-65535           // <port ranges>: Only scan specified ports; Example: -p1-65535;
#-oA                 // <basename>: Output in the three major formats at once
#"""
