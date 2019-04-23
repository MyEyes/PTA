import nmap
import sys
import os
import json
import sqlite3

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
    c = conn.cursor()
    c.execute("INSERT INTO project  VALUES (NULL, '" + name + "', '" + hosts + "', '" + ports + "', '" + prots + "')")
    conn.commit()

def load_proj():
    global data
    c = conn.cursor()
    for row in c.execute("SELECT * FROM projects ORDER BY id"):
        print(row)

def run_nmap():
    global data
    nm = nmap.PortScanner() # init
    nm.scan(hosts=data['project'][0]['hosts'], ports=data['project'][0]['ports'])
    print(nm.scan_result())

def output_projname():
    path = './proj/'
    dirs = os.listdir(path) # Ausgabe aller Projektnamen
    i=0
    for file in dirs:
        print("[" + str(i) + "] " + file.replace('.pta', ''))
        i = i + 1

# start
clrs()
p_logo()

#conn = None


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
        "'prots' INTEGER);")
    c.execute("CREATE TABLE 'r_nmap' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"\
        "'host'  TEXT NOT NULL UNIQUE, "\
        "'protocol' TEXT, "\
        "'port' INTEGER, "\
        "'name' TEXT,"\
        "'state' TEXT,"\
        "'product' TEXT,"\
        "'extrainfo' TEXT,"\
        "'reason' TEXT,"\
        "'version' TEXT,"\
        "'conf' TEXT);")
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



    print("which project would you like to load?")
    i_proj  = input("proj: ") # projekt welches geladen werden soll eingeben

    load_proj(i_proj)
    clrs()
    p_logo()

    print("actual project: " + data['project'][0]['name'])
    print("options: ")
    print("[0] scan all")
    print("[x] show report")
    print("[x] change modules")
    i_nr = input("option: ")

    if i_nr == "0":
        run_nmap()

######################################################################
elif i_nr == "3": # Funktion: Projekt löschen
    clrs()
    p_logo()
    print("which project would you like to delete?")

    output_projname()

    i_nr = input("your input:") #löschendes projekt auswählen

    i=0
    i_proj=None
    for file in dirs:
            if i==int(i_nr):
                i_proj=file.replace('.pta', '')
            i = i + 1

    if i_proj != None:
        if os.path.exists("./proj/" + i_proj + ".pta"):
            os.remove("./proj/" + i_proj + ".pta")
            print("the project " + i_proj + " has been removed") # projekt wird gelöscht
    else:
        print("The Project " + i_nr + " does not exist")
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
