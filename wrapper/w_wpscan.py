import os
import sys
import requests
import json
from random import randint

# sys.argv[1] => hostname/ ip
# sys.argv[2] => port
# sys.argv[3] => outf (output file)
# sys.argv[4] => wordl (wordlist)

hostname    = sys.argv[1]
port        = sys.argv[2]
outf        = sys.argv[3]
#wordl       = sys.argv[4]

sid = randint(1000000000, 9999999999)
sid = str(sid)
pre = ""

### check, if http or https
try:
    r = requests.get("https://" + hostname + ":" + port)
    pre = "https"

except:
    # no https
    try:
        r = requests.get("http://" + hostname + ":" + port)
        pre = "http"
    except:
        # no http
        pass

if (pre != ""):
    os.system("wpscan --url " + pre + "://" + hostname + ":" + port + " -f json -o wpscan_" + sid)
    print(pre)
    print(hostname)
    print(port)
    with open("wpscan_" + sid, 'r') as file_in:
        f = open(outf, 'w')
        data = json.load(file_in)
        for x in data['interesting_findings']:
            f.write(x)

        f.close()
    #os.remove("wpscan_" + sid)
