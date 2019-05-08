from db import conn
import project
import modules

_modules = modules.load_modules()

def scan():
    global _modules
    c = conn.cursor()
    c.execute("SELECT * FROM r_nmap WHERE pid=" + str(project.current[0]) + " AND status=0;")
    rows = c.fetchall()
    for row in rows:
        print(row)
        i=0
        for _module in _modules:
            _module.Run(i, row[4], row[7])
            i += 1

        # this row is completed! mark it in the status column
        c.execute("UPDATE r_nmap SET status = 1 WHERE id=" + str(row[0]) + ";")
        conn.commit()