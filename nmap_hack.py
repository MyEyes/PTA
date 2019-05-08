from db import conn
import nmap
import os
import datetime
import project
#--------------------------------------------------------------------#
def run_nmap(): # function to run nmap scan
    c = conn.cursor()
    return #TODO: Remove this, only here because the standard nmap package doesn't seem to implement this functionality
    nm = nmap.PortScanner() # init
    #Hardcode this or employ proper configuration for stuff
    nm.scan(hosts=project.current[2], ports=project.current[3], arguments=settings[int(project.current[4])])

    iternmcsv = iter(nm.csv().splitlines())
    next(iternmcsv)
    for row in iternmcsv:
        if(row.split(';')[6] == "open"):
            cmd = "INSERT INTO r_nmap VALUES (NULL, " + str(project.current[0]) + ", datetime('now', 'localtime')"
            for entr in row.split(';'):
                cmd += ", '" + entr + "'"
            cmd += ", 0);"
            c.execute(cmd)

    conn.commit()