import nmap
import sys
import os
import sqlite3
import csv

# TODO
# - delete database & reload modules.cfg
#   -> sqlite datei löschen und programm neustarten
# - zurück gehen im terminal?
# nach dem das projekt geladen wurde:
#   change module -> aufspalten in add module und delete module

# GLOBALS
conn = None
proj = None
_mod = []

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

def sqll_create_table(name, n):
    global data
    global conn

    c = conn.cursor()
    cmd = "CREATE TABLE 'r_" + name + "' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 'pid'  INTEGER"

    for i in range(n):
        cmd += ", '" + str(i) + "'  TEXT"

    cmd += ");"
    c.execute(cmd)
    conn.commit()

def load_proj(name):
    global proj
    c = conn.cursor()
    c.execute("SELECT * FROM project WHERE name='" + name + "'")
    rows = c.fetchall()
    proj = rows[0]

def sqll_ins(table, arr):
    global conn
    cmd = "INSERT INTO " + table + " VALUES (NULL, " + str(proj[0])
    for entr in arr:
        cmd = cmd + ", '" + entr + "'"
    cmd = cmd + ");"

    c = conn.cursor()
    c.execute(cmd)
    conn.commit()

def run_nmap():
    global proj
    global connect
    global nmpar

    c = conn.cursor()
    nm = nmap.PortScanner() # init
    nm.scan(hosts=proj[2], ports=proj[3], arguments=nmpar)

    iternmcsv = iter(nm.csv().splitlines())
    next(iternmcsv)
    for row in iternmcsv:
        cmd = "INSERT INTO r_nmap VALUES (NULL, " + str(proj[0])
        for entr in row.split(';'):
            cmd = cmd + ", '" + entr + "'"
        cmd = cmd + ", 0);"
        c.execute(cmd)

    conn.commit()

def run_cmd(mid, hostname, port):
    global proj
    global _mod

    os.system(_mod[mid][3].replace("$ip", hostname).replace("$port", port))

    reader = csv.reader(open("tmp.csv", 'r'), delimiter=_mod[mid][4][0])
    itercsv = iter(reader)
    next(itercsv)
    for row in itercsv:
        if(int(_mod[mid][2]) == len(row)):
            sqll_ins("r_" + _mod[mid][0], row)

    os.remove("tmp.csv")

def working():
    global conn
    global proj
    global _mod

    c = conn.cursor()
    c.execute("SELECT * FROM r_nmap WHERE pid=" + str(proj[0]) + " AND status=0;")
    rows = c.fetchall()
    for row in rows:
        print(row)
        i=0
        for _module in _mod:
            if(row[7] == _module[1]):
                run_cmd(i, row[2], row[6])
            i += 1

        # this row is completed! mark it in the status column
        c.execute("UPDATE r_nmap SET status = 1 WHERE id=" + str(row[0]) + ";")
        conn.commit()



# start
clrs()
p_logo()

### LOAD cfg
with open('modules.cfg') as fp:
    i = 0
    for row in fp:
        if (i==0):
            nmpar = row
        else:
            _mod.append(row.split('<#>'))
        i += 1
###

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
        "'cpe' TEXT,"\
        "'status' INTEGER DEFAULT 0);")

    conn.commit()


    print(_mod)
    for yo in _mod:
        sqll_create_table(yo[0], int(yo[2]))

print("Menu:")
print("0     : exit programm")
print("1     : create project")
print("2     : load project")
print("3     : delete project")
print("4     : delete database & reload modules")

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
    c.execute("SELECT * FROM project ORDER BY id")
    rows = c.fetchall()
    for row in rows:
        print("[" + str(i) + "] " + row[1])
        i = i + 1

    print("which project would you like to load?")
    i_proj  = input("proj: ")

    load_proj(i_proj)
    clrs()
    p_logo()

    print("actual project: " + proj[1])
    print("options: ")
    print("[0] scan all")
    print("[1] resume")
    print("[2] nmap only")
    i_nr = input("option: ")

    if i_nr == "0":
        run_nmap()
        working()
        ###########
    elif i_nr == "1":
        working()
    elif i_nr == "2":
        run_nmap()



######################################################################
elif i_nr == "3": # delete project
    clrs()
    p_logo()
    print("which project would you like to delete?")

    i=0
    c = conn.cursor()
    c.execute("SELECT * FROM project ORDER BY id")
    rows = c.fetchall()
    for row in rows:
        print("[" + str(i) + "] " + row[1])
        i = i + 1

    i_nr = input("your input:") #löschendes projekt auswählen

    sql = "DELETE FROM project WHERE name='" + i_nr + "'"
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    print(i_nr + " was delete")
######################################################################
elif i_nr == "4":
    #datenbank wird gelöscht und die Module werden neu geladen
    clrs()
    p_logo()
    print("delete database")
    print("Confirm deletion with y: ")
    i_load=input()
    if (i_load.lower() == "y"):
        os.remove("pta.sqlite")
        os.system("python3 pta.py")

#
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
