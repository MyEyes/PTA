import os
import sys

projectn    = sys.argv[1]
filename    = sys.argv[2]

with open("./projects/" + projectn + "/" + filename, 'r') as f_in:
    with open("./projects/" + projectn + "/findings.csv", 'a') as f_out:
        for x in f_in:
            f_out.write(x)
