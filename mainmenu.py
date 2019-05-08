import menu
from logo import print_logo
import project
from db import conn
import shutil
import os
import sys

def CreateMainMenu():
    mainmenu = menu.Menu("Main Menu")
    mainmenu.addItem(menu.MenuItem("exit program", mm_exit))
    mainmenu.addItem(menu.MenuItem("create project", mm_createProj))
    mainmenu.addItem(menu.MenuItem("load project", mm_loadProj))
    mainmenu.addItem(menu.MenuItem("delete project", mm_delProj))
    mainmenu.addItem(menu.MenuItem("wipe", mm_wipe))
    return mainmenu

def mm_exit():
    exit()

def mm_createProj():
    #This is horrible practice you should create a submenu for this instead and this dialogue should be a project menu or whatever
    i_abfrage="c" # so that the program can enter the while loop once.

    while (i_abfrage.lower() == "c"): # to create another project
        print_logo()
        print("create project")
        print("------------------------------------------")
        i_proj      = input("project name: ")
        i_hosts     = input("hosts (ip): ")
        i_prot      = input("TCP (0) or UDP (1): ")
        i_port      = input("ports: ")
        i_http_s    = input("http (0) or https (1): ")
        print("")
        project.create(i_proj, i_hosts, i_port, i_prot, i_http_s)
        print_logo()
        print("create a project")
        print("------------------------------------------")
        print("project: " + i_proj + " successfully create")
        print("")
        print("press 'r' to return menu:") # open the complete py script
        print("press 'l' to load the project:")
        print("press 'c' to create another project:") # while i_abfrage = c

        i_abfrage=input()
    if (i_abfrage.lower() == "r"): # after creating a project, the py script starts against
        return
    elif (i_abfrage.lower() == "l"):
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM project;")
        project.load(str(int(c.fetchone()[0])-1)) # load project created above

def mm_loadProj():
    print_logo()
    print("load project")
    print("------------------------------------------")
    print("which project would you like to load?")
    print("")
    i=0
    c = conn.cursor()
    c.execute("SELECT * FROM project")
    rows = c.fetchall()
    for row in rows:
        print(str(i) + "     : " + row[1])
        i = i + 1

    print("")
    i_proj  = input("projectname: ")

    project.load(i_proj)

def mm_delProj():
    print_logo()
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

    project.delete(rows[i_nr])
        
def mm_wipe():
    print_logo()
    print("delete database & reload modules")
    print("------------------------------------------")
    print("")
    print("press 'y' to confirm deletion: ")
    i_load=input()
    if (i_load.lower() == "y"):
        print("Deleting")
        os.remove("pta.sqlite")
        shutil.rmtree("./projects")
        os.system("python3 pta.py")
        return
    print("Aborted")