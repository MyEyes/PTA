import os
import sys

#os.system("dirb https://" + sys.argv[1] + ":" + sys.argv[2] + " -f -o lol.txt")

with open('dirb_ausgabe_in.txt', 'r') as file_in:
    for x in file_in:
        if((x[0] == '=') | (x[0:3] == "+ h")):
            print(x)
