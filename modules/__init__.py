import os
import importlib
import sys

def load_modules():
    modules = []
    print("Loading modules")
    for filename in os.listdir("modules"):
        sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
        if filename.endswith(".py") and filename!="__init__.py":
            module = importlib.import_module("modules."+filename[:-3])
            module_class = getattr(module, "Module")
            instance = module_class()
            modules.append(instance)
    print(modules)
    return modules