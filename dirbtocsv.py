import os
import shutil

os.execute("dirb " + sys.arg[1] + ":" + sys.arg[2])

with open('dirb_ausgabe_in.txt', 'rb') as file_in:
    with open("dirb_ausgabe_out1.csv", "wb") as file_out1:
        file_out1.writelines(filter(lambda line: b'=' in line, file_in))
s = open("dirb_ausgabe_out1.csv").read()
s = s.replace('==> DIRECTORY: ', '')
f = open("dirb_ausgabe_out1.csv", 'w')  # ersetzt "==> DIRECTORY: " mit "" da wir nur die URL haben wollen
f.write(s)
f.close()

with open('dirb_ausgabe_in.txt', 'rb') as file_in:
    with open("dirb_ausgabe_out2.csv", "wb") as file_out2:
        file_out2.writelines(filter(lambda line: b'+' in line, file_in))
s = open("dirb_ausgabe_out2.csv").read()
s = s.replace('+ ', '')
f = open("dirb_ausgabe_out2.csv", 'w')  # ersetzt "+ " mit "" da wir nur die URL haben wollen
f.write(s)
f.close()

with open('dirb_ausgabe_final.csv','wb') as AABB: # fusioniert beide csv dateien
    for f in ['dirb_ausgabe_out1.csv','dirb_ausgabe_out2.csv']:
        with open(f,'rb') as bbaa:
            shutil.copyfileobj(bbaa, AABB)
