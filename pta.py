import nmap
import sys
import os
import sqlite3
import csv
import atexit
from termcolor import colored
from random import randint

# TODO
# beim start: stty icanon
# beim beenden: stty -icanon

# GLOBALS
conn = None
proj = None
_mod = []
sid  = randint(1000000000, 9999999999)
#--------------------------------------------------------------------#
def exit_handler():
    os.system('stty -icanon')
atexit.register(exit_handler)
os.system('stty icanon')
#--------------------------------------------------------------------#
def clrs(): # this command clear the terminal
    os.system('clear')
#--------------------------------------------------------------------#
def p_logo(): # the logo was defined here
    print(colored('PTA - PenTestAutomatizer version 0.5\n', 'blue'))
    print(colored("PPPPPP    TTTTTTTTT      A", "red"))
    print(colored("PP  PPP   TTTTTTTTT     AAA", "red"))
    print(colored("PP  PPP      TTT       AA AA", "red"))
    print(colored("PPPPPP       TTT      AA   AA", "red"))
    print(colored("PPP          TTT     AAAAAAAAA", "red"))
    print(colored("PPP          TTT    AAAAAAAAAAA", "red"))
    print(colored("PPP          TTT   AAAA     AAAA\n", "red"))
#--------------------------------------------------------------------#
def ShowProjDelProj(): # shows all projects and deletes a selected project
    clrs()
    p_logo()
    print("delete a project")
    print("------------------------------------------")
    print("which project would you like to delete?")
    print("")
    i=0
    c = conn.cursor()
    c.execute("SELECT * FROM project ORDER BY id")
    rows = c.fetchall()
    for row in rows:
        print(str(i) + "     : " + row[1])
        i = i + 1

    i_nr = input("projectname: ") # choose a projekt to delete

    sql = "DELETE FROM project WHERE name='" + i_nr + "'"
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
#--------------------------------------------------------------------#
def create_p(name, hosts, ports, prots): # function to create a project
    global data
    c = conn.cursor()
    c.execute("INSERT INTO project  VALUES (NULL, '" + name + "', '" + hosts + "', '" + ports + "', '" + prots + "')")
    conn.commit()
#--------------------------------------------------------------------#
def sqll_create_table(name, n): # creating of a sql database
    global data
    global conn

    c = conn.cursor()
    cmd = "CREATE TABLE 'r_" + name + "' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 'pid'  INTEGER"

    for i in range(n):
        cmd += ", '" + str(i) + "'  TEXT"

    cmd += ");"
    c.execute(cmd)
    conn.commit()
#--------------------------------------------------------------------#
def load_proj(name): # function to load a project
    global proj
    c = conn.cursor()
    c.execute("SELECT * FROM project WHERE name='" + name + "'")
    rows = c.fetchall()
    proj = rows[0]
#--------------------------------------------------------------------#
def sqll_ins(table, arr):
    global conn
    cmd = "INSERT INTO " + table + " VALUES (NULL, " + str(proj[0])
    for entr in arr:
        cmd = cmd + ", '" + entr + "'"
    cmd = cmd + ");"

    c = conn.cursor()
    c.execute(cmd)
    conn.commit()
#--------------------------------------------------------------------#
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
#--------------------------------------------------------------------#
def run_cmd(mid, hostname, port):
    global proj
    global _mod

    os.system(_mod[mid][3].replace("$ip", hostname).replace("$port", port).replace("$out", "tmp_" + str(sid) + ".csv"))

    print(str(mid) + "\n" + "tmp_" + str(sid) + ".csv\nlol")

    reader = csv.reader(open("tmp_" + str(sid) + ".csv", 'r'), delimiter=_mod[mid][4][0])
    itercsv = iter(reader)
    next(itercsv)
    for row in itercsv:
        if(int(_mod[mid][2]) == len(row)):
            sqll_ins("r_" + _mod[mid][0], row)

    os.remove("tmp_" + str(sid) + ".csv")
#--------------------------------------------------------------------#
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
                run_cmd(i, row[3], row[6])
            i += 1

        # this row is completed! mark it in the status column
        c.execute("UPDATE r_nmap SET status = 1 WHERE id=" + str(row[0]) + ";")
        conn.commit()
#--------------------------------------------------------------------#
# programm starts here
clrs()
p_logo()

#---- LOAD modules.cfg begin----#
with open('modules.cfg') as fp:
    i = 0
    for row in fp:
        if (i==0):
            nmpar = row
        else:
            _mod.append(row.split('<#>'))
        i += 1
#---- LOAD modules.cfg end----#

if os.path.exists("./pta.sqlite"): # creating sql database
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

print("main menu:")
print("------------------------------------------")
print("0     : exit this programm")
print("1     : create a project")
print("2     : load a project")
print("3     : delete a project")
print("4     : delete the database and reload the modules")
print("------------------------------------------")
i_nr=input()
######################################################################
if i_nr == "0": # exit the programm
    clrs()
    p_logo()
    print("exit this programm")
    print("------------------------------------------")
    print("you have successfully quit the programm!")
    sys.exit()
######################################################################
elif i_nr == "1": # create a project
    clrs()
    p_logo()
    print("create a project")
    print("------------------------------------------")
    i_proj  = input("project name: ")
    i_hosts = input("hosts (ip): ")
    i_prot  = input("TCP (0) or UDP (1) or BOTH (2): ")
    i_port  = input("ports : ")
    print("")
    create_p(i_proj, i_hosts, i_port, i_prot)
    clrs()
    p_logo()
    print("create a project")
    print("------------------------------------------")
    print("you have successfully create the project: " + i_proj)
    print("")
    print("press C to continue:")
    i_cont=input()  # after creating a project, the programm starts against
    if (i_cont.lower() == "c"):
        os.system("python3 pta.py")
######################################################################
elif i_nr == "2": # load a project
    clrs()
    p_logo()
    print("load a project")
    print("------------------------------------------")
    print("which project would you like to load?")
    print("")
    i=0
    c = conn.cursor()
    c.execute("SELECT * FROM project ORDER BY id")
    rows = c.fetchall()
    for row in rows:
        print(str(i) + "     : " + row[1])
        i = i + 1

    print("")
    i_proj  = input("projectname: ")

    load_proj(i_proj)
    clrs()
    p_logo()
    print("load a project")
    print("------------------------------------------")
    print("the project: " + proj[1] + " has been loaded")
    print("")
    print("options: ")
    print("")
    print("0     : scan all")
    print("1     : resume")
    print("2     : nmap only")
    print("------------------------------------------")
    i_nr = input("option: ")

    if i_nr == "0": # scan all
        run_nmap()
        working()
        ###########
    elif i_nr == "1": # resume
        working()
    elif i_nr == "2": # nmap only
        run_nmap()

######################################################################
elif i_nr == "3": # delete a project

    ShowProjDelProj() # shows all projects and deletes a selected project

    clrs()
    p_logo()
    print("delete a project")
    print("------------------------------------------")
    print("you have successfully delete the project: " + i_nr)
    print("")
    print("press c to go back in the main menu:")
    print("                or                 ")
    print("press d to delete another project:")

    i_abfrage=input()

    while (i_abfrage.lower() == "d"): # to delete another project
        ShowProjDelProj()
        clrs()
        p_logo()
        print("delete a project")
        print("------------------------------------------")
        print("you have successfully delete the project: " + i_nr)
        print("")
        print("press c to go back in the main menu:")
        print("         or         ")
        print("press d to delete another project:")
        i_abfrage=input()
    if (i_abfrage.lower() == "c"): # to go back in the menu
        os.system("python3 pta.py")
######################################################################
elif i_nr == "4": # the database is deleted and the modules are reloaded
    clrs()
    p_logo()
    print("delete the database and reload the modules")
    print("------------------------------------------")
    print("")
    print("Confirm deletion with y: ")
    i_load=input()
    if (i_load.lower() == "y"):
        os.remove("pta.sqlite")
        os.system("python3 pta.py")
######################################################################
