import os
import sys
import string


#os.system("dirb https://" + sys.argv[1] + ":" + sys.argv[2] + " -f -o lol.txt")

with open('dirb_ausgabe_in.txt', 'r') as file_in:
    f = open("dirb_" + sys.argv[3] + ".csv", 'w')
    for x in file_in:
        if(x[0:3] == "==>"):
            # dir
            f.write(x[15:])
        elif(x[0:3] == "+ h"):
            #file
            f.write(x[2:])

    f.close()
