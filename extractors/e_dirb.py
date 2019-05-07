import os
import sys

projectn    = sys.argv[1]
filename    = sys.argv[2]

with open("./projects/" + projectn + "/" + filename, 'r') as file_in:
    with open("./projects/" + projectn + "/dirb.", 'a') as file_out:
        for x in file_in:
            if(x[0:3] == "==>"):
                # dir
                str_=x[15:-1] + ";dir\n"
                print(str_)
                #file_out.write(str_)
            elif(x[0:3] == "+ h"):
                #file
                str_=x[2:-1] + ";file\n"
                print(str_)
                #file_out.write(str_)
