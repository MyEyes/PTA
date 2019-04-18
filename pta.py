aimport nmap # import nmap.py module
import sys
import os
import json
def clrs():
    os.system('clear')

clrs();
print("PTA - PenTestAutomatizer version 0.1 alpha\n") # to run:  python3 /root/Documents/pythonfolder/hello.py
print("PPPPPP    TTTTTTTTT      A")
print("PP  PPP   TTTTTTTTT     AAA")
print("PP  PPP      TTT       AA AA")
print("PPPPPP       TTT      AA   AA")
print("PPP          TTT     AAAAAAAAA")
print("PPP          TTT    AAAAAAAAAAA")
print("PPP          TTT   AAAA     AAAA\n")

print("Menu:")
print("0     : exit programm")
print("1     : start programm")
print("2     : load project")
print("3     : delete project")

eingabe=input()
if eingabe == "0":
    sys.exit()
elif eingabe == "1":
    clrs();
    print("programm start")
    print("Give the name of your project:")
elif eingabe == "2":
    clrs();
    print("programm1 ausgewählt")
elif eingabe == "3":
    clrs();
    print("programm2 ausgewählt")
else:
    print("please enter a valid value")
    eingabe = input("your input:")
    clrs();

"""erklärung fü uns
nmap -sS -sV -sC -Pn -n -vv -O -p1-65535 -oA nmapscan_full_tcp_$IP <ip | domain>
-sS                 // TCP SYN
-sV                 // Probe open ports to determine service/version info
-sC                 // equivalent to --script=default
--script=<yolo>     // <yolo> is a comma separated list of directories, script-files or script-categories
-Pn                 // Treat all hosts as online -- skip host discovery
-n                  // -n/-R: Never do DNS resolution/Always resolve [default: sometimes]
-v                  // Increase verbosity level (use -vv or more for greater effect)
-O                  // -O: Enable OS detection
-p1-65535           // <port ranges>: Only scan specified ports; Example: -p1-65535;
-oA                 // <basename>: Output in the three major formats at once

"""
