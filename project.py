from logo import print_logo
import os
import shutil
import nmap_hack
import report
import scan
from db import conn

#This is a dirty hack, there should be a project class and objects of that type being passed around instead of global variables
current = None

def projects_init():
    if not os.path.exists("./projects/"):
        os.mkdir("./projects/")

def create(name, hosts, ports, prots, http_s): # function to create a project
    c = conn.cursor()
    c.execute("INSERT INTO project  VALUES (NULL, '" + name + "', '" + hosts + "', '" + ports + "', '" + prots + "', '" + http_s + "');")
    conn.commit()
    os.makedirs("./projects/" + name)
#--------------------------------------------------------------------#
def load(proj_n): # function to load a project
    global current
    c = conn.cursor()
    c.execute("SELECT * FROM project;")
    rows = c.fetchall()
    current = rows[int(proj_n)]

    print_logo()

    print("load project")
    print("------------------------------------------")
    print("project: " + current[1] + " loaded")
    print("")
    print("options: ")
    print("")
    print("0     : scan all")
    print("1     : resume")
    print("2     : nmap only")
    print("3     : create report")
    print("------------------------------------------")
    i_nr = input("option: ") # choose one option

    if i_nr == "0": # scan all
        nmap_hack.run_nmap()
        scan.scan()
        ###########
    elif i_nr == "1": # resume
        scan.scan()
    elif i_nr == "2": # nmap only
        nmap_hack.run_nmap()
    elif i_nr == "3": # create report
        report.create(current[1])
    elif (i_nr != "0" or "1" or "2" or "3"):
        print("enter a valid value!")
#--------------------------------------------------------------------#


def delete(name):
    #This function should return a value indicating success of failure
    sql = "DELETE FROM project WHERE name='" + name + "';"
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    shutil.rmtree("./projects/" + name + "/")