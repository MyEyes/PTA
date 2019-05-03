import os
import sys
import requests
from random import randint

# sys.argv[1] => hostname/ ip
# sys.argv[2] => port
# sys.argv[3] => outf (output file)
# sys.argv[4] => wordl (wordlist)

hostname    = sys.argv[1]
port        = sys.argv[2]
outf        = sys.argv[3]
wordl       = sys.argv[4]

sid = randint(1000000000, 9999999999)
sid = str(sid)
pre = ""

### check, if http or https
try:
    r = requests.get("http://" + hostname + ":" + port)
    pre = "http"
except:
    # no http
    try:
        r1 = requests.get("https://" + hostname + ":" + port)
        pre = "https"
    except:
        # no https
        pass

if (pre != ""):
    os.system("dirb " + pre + "://" + hostname + ":" + port + " " + wordl +  " -f -o dirb_" + sid + ".txt")

    with open("dirb_" + sid + ".txt", 'r') as file_in:
        f = open(outf, 'w')
        for x in file_in:
            if(x[0:3] == "==>"):
                # dir
                f.write(x[15:-1] + ";dir\n")
            elif(x[0:3] == "+ h"):
                #file
                f.write(x[2:-1] + ";file\n")

        f.close()
    os.remove("dirb_" + sid + ".txt")
