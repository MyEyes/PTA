class Module:
    def __init__(self):
        print("Initialized test module")

    def Run(self, mid, hostname, port):
        print("Module invoked on %s:%d"%(hostname,port))