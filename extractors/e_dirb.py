import os
import sys

projectn    = sys.argv[1]
filename    = sys.argv[2]

with open("./projects/" + projectn + "/" + filename, 'r') as f_in:
    with open("./projects/" + projectn + "/findings.csv", 'a') as f_out:
        f_out.write('lol')
        for x in f_in:
            if(x[0:3] == "==>"):
                # dir
                str_=x[15:-1] + ";dir\n"
                f_out.write(str_)
            elif(x[0:3] == "+ h"):
                #file
                str_=x[2:-1] + ";file\n"
                f_out.write(str_)
        f_out.write('\n')
