import os
def create(proj_name):
    for f in os.listdir("./projects/" + proj_name + "/"):
        if f != "findings.csv":
            os.system("python3 ./extractors/e_" + f.split('_')[2].split('.')[0] + ".py " + proj_name + " " + f)