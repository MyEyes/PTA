import os
import sys
import requests
from random import randint

projectn    = sys.argv[1]
datatype    = sys.argv[2]

with open("./projects/" + projectn + "/dirb." + datatype, 'r') as file_in:
    f = open("./projects/" + projectn + "/dirb_findings.txt", 'w')
    for x in file_in:
        if(x[0:3] == "==>"):
            # dir
            str_=x[15:-1] + ";dir\n"
            f.write(str_)
        elif(x[0:3] == "+ h"):
            #file
            str_=x[2:-1] + ";file\n"
            f.write(str_)

    f.close()
