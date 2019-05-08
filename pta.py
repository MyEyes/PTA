import nmap, sys, csv
import sqlite3, os
import hashlib, atexit
import json
import shutil
import datetime
from termcolor import colored
from random import randint
from logo import *
import menu
import mainmenu
import project
import modules
from db import conn
#--------------------------------------------------------------------#
# GLOBALS
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
# main programm starts here!
#clrs()
print_logo()
#---- LOAD modules.cfg end----#

mm = mainmenu.CreateMainMenu()

while True:
    mm.DoDialog()