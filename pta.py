import nmap, sys, csv
import sqlite3, os
import hashlib, atexit
import json
import shutil
from termcolor import colored
from random import randint
from datetime import datetime
#--------------------------------------------------------------------#
# GLOBALS
conn        = None
proj        = None
settings    = [None]*3
_mod        = []
sid         = randint(1000000000, 9999999999) # Return a random integer N such that a <= N <= b.
#--------------------------------------------------------------------#
def exit_handler(): # function to go back during terminal input
    os.system('stty -icanon')
atexit.register(exit_handler)
os.system('stty icanon')
#--------------------------------------------------------------------#
def clrs(): # this command clear the terminal
    os.system('clear')
#--------------------------------------------------------------------#
def p_logo(): # the logo was defined here
    print(colored('PenTestAutomatizer\n', 'blue'))
    print(colored(" ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ ", "red"))
    print(colored("▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌", "red"))
    print(colored("▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌", "red"))
    print(colored("▐░▌       ▐░▌     ▐░▌     ▐░▌       ▐░▌", "red"))
    print(colored("▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌", "red"))
    print(colored("▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌", "red"))
    print(colored("▐░█▀▀▀▀▀▀▀▀▀      ▐░▌     ▐░█▀▀▀▀▀▀▀█░▌", "red"))
    print(colored("▐░▌               ▐░▌     ▐░▌       ▐░▌", "red"))
    print(colored("▐░▌               ▐░▌     ▐░▌       ▐░▌", "red"))
    print(colored(" ▀                 ▀       ▀         ▀ \n", "red"))
#--------------------------------------------------------------------#
def create_p(name, hosts, ports, prots, http_s): # function to create a project
    with open('projects.csv', 'a') as f:
        f.write(name + ";" + hosts + ";" + ports + ";" + prots + ";" + http_s + "\n")
    os.makedirs("./projects/" + name)
#--------------------------------------------------------------------#
def sqll_create_table(name, n): # function to create a sql database
    global data
    global conn

    c = conn.cursor()
    cmd = "CREATE TABLE 'r_" + name + "' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 'pid'  INTEGER, 'datetime' TEXT"

    for i in range(n):
        cmd += ", '" + str(i) + "'  TEXT"

    cmd += ");"
    c.execute(cmd)
    conn.commit()
#--------------------------------------------------------------------#
def load_proj(proj_n): # function to load a project
    global proj
    with open('projects.csv') as csvfile:
        projects = csv.reader(csvfile, delimiter=';')
        i=0
        for row in projects:
            if(i==int(proj_n)):
                proj = row
                break
            i+=1

    clrs()
    p_logo()
    print("load project")
    print("------------------------------------------")
    print("project: " + proj[1] + " loaded")
    print("")
    print("options: ")
    print("")
    print("0     : scan all")
    print("1     : resume")
    print("2     : nmap only")
    print("------------------------------------------")
    i_nr = input("option: ") # choose one option

    if i_nr == "0": # scan all
        run_nmap()
        working()
        ###########
    elif i_nr == "1": # resume
        working()
    elif i_nr == "2": # nmap only
        run_nmap()
    elif (i_nr != "0" or "1" or "2"):
        print("enter a valid value!")
    elif (i_abfrage.lower() != "r" or "l" or "c"):
        print("enter a valid value!")
#--------------------------------------------------------------------#
def sqll_ins(table, arr): #
    global conn
    cmd = "INSERT INTO " + table + " VALUES (NULL, " + str(proj[0]) + ", datetime('now', 'localtime')"
    for entr in arr:
        cmd = cmd + ", '" + entr + "'"
    cmd = cmd + ");"

    c = conn.cursor()
    c.execute(cmd)
    conn.commit()
#--------------------------------------------------------------------#
def run_nmap(): # function to run nmap scan
    global proj
    global settings

    nm = nmap.PortScanner() # init
    nm.scan(hosts=proj[1], ports=proj[2], arguments=settings[int(proj[3])])

    iternmcsv = iter(nm.csv().splitlines())
    next(iternmcsv)

    with open("./projects/" + proj[0] + "/nmap.csv", 'a') as f:
        for row in iternmcsv:
            lol=str(datetime.now())  + ";"
            lol+=row
            if(row.split(';')[6] == "open"):
                lol += "; 0"
            else:
                lol += "; 1"
            lol+="\n"
            f.write(lol)
#--------------------------------------------------------------------#
def run_cmd(mid, hostname, port):
    global proj
    global _mod

    os.system(_mod[mid][3].replace("$ip", hostname).replace("$port", port).replace("$out", "./projects/" + proj[0] + "/" + _mod[mid][0] + "." + _mod[mid][3]))
#--------------------------------------------------------------------#
def working():
    global proj
    global _mod

    with open("./projects/" + proj[0] + "/nmap.csv", 'a') as f:
        projects = csv.reader(f, delimiter=';')
        for row in rows:
            print(row)
            input()
            i=0
            for _module in _mod:
                if(row[8] == _module[1]):
                    run_cmd(i, row[4], row[7])
                i += 1

        # this row is completed! mark it in the status column
        c.execute("UPDATE r_nmap SET status = 1 WHERE id=" + str(row[0]) + ";")
        conn.commit()
#--------------------------------------------------------------------#
# main programm starts here!
clrs()
p_logo()

#---- LOAD modules.cfg begin----#
with open('modules.cfg') as fp:
    for row in fp:
        _mod.append(row.split('<#>'))

with open('settings.cfg') as fp:
    i=0
    for row in fp:
        settings[i] = str(row[:-1])
        i+=1
#---- LOAD modules.cfg end----#
if not os.path.exists("./projects.csv"):
    open("projects.csv", 'a').close()

if not os.path.exists("./projects/"):
    os.mkdir("./projects/")

print("main menu:")
print("------------------------------------------")
print("0     : exit programm")
print("1     : create project")
print("2     : load project")
print("3     : delete project")
print("4     : delete database & reload modules")
print("------------------------------------------")
i_nr=input()

######################################################################
if i_nr == "0": # exit the programm
    clrs()
    p_logo()
    print("exit programm")
    print("------------------------------------------")
    print("successfully quit programm!")
    sys.exit()
######################################################################
elif i_nr == "1": # create a project
    i_abfrage="c" # so that the program can enter the while loop once.

    while (i_abfrage.lower() == "c"): # to create another project
        clrs()
        p_logo()
        print("create project")
        print("------------------------------------------")
        i_proj      = input("project name: ")
        i_hosts     = input("hosts (ip): ")
        i_prot      = input("TCP (0) or UDP (1): ")
        i_port      = input("ports: ")
        i_http_s    = input("http (0) or https (1): ")
        print("")
        create_p(i_proj, i_hosts, i_port, i_prot, i_http_s)
        clrs()
        p_logo()
        print("create a project")
        print("------------------------------------------")
        print("project: " + i_proj + " successfully create")
        print("")
        print("press 'r' to return menu:") # open the complete py script
        print("press 'l' to load the project:")
        print("press 'c' to create another project:") # while i_abfrage = c

        i_abfrage=input()
    if (i_abfrage.lower() == "r"): # after creating a project, the py script starts against
        os.system("python3 pta.py")
    elif (i_abfrage.lower() == "l"):
        num_lines = sum(1 for line in open("projects.csv"))
        load_proj(str(int(num_lines-1))) # load project created above

######################################################################
elif i_nr == "2": # load a project
    clrs()
    p_logo()
    print("load project")
    print("------------------------------------------")
    print("which project would you like to load?")
    print("")
    i=0
    with open('projects.csv') as csvfile:
        projects = csv.reader(csvfile, delimiter=';')
        for row in projects:
            print(str(i) + "     : " + row[0])
            i = i + 1

    print("")
    i_proj  = input("projectname: ")

    load_proj(i_proj)
######################################################################
elif i_nr == "3": # delete a project
    i_abfrage="d"# so that the program can enter the while loop once.

    while (i_abfrage.lower() == "d"): # to delete a project
        clrs()
        p_logo()
        print("delete project")
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

        clrs()
        p_logo()
        print("delete project")
        print("------------------------------------------")
        print("project: " + i_nr + " successfully delete")
        print("")
        print("press 'r' to return main menu:")
        print("press 'd' to delete another project:") # it is spring back to the while loop

        i_abfrage=input()
    if (i_abfrage.lower() == "r"): # to go back in the menu
        os.system("python3 pta.py")
    elif (i_abfrage.lower() != "r" and i_abfrage.lower() !=  "d"):
        print("enter a valid value!")
######################################################################
elif i_nr == "4": # the database is deleted and the modules are reloaded
    clrs()
    p_logo()
    print("delete database & reload modules")
    print("------------------------------------------")
    print("")
    print("press 'y' to confirm deletion: ")
    i_load=input()
    while (i_load != "y"):
        print("enter a valid value!")
        i_load=input()
    if (i_load.lower() == "y"):
        os.remove("projects.csv")
        shutil.rmtree("./projects")
        os.system("python3 pta.py")
######################################################################
elif i_nr != "1" or "2" or "3" or "4": # if you give an false input, programm start new
    os.system("python3 pta.py")
######################################################################
