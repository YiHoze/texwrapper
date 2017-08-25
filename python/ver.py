import sys
import pip
import importlib.util

installed_packages = pip.get_installed_distributions()
if len(sys.argv) > 1:
    package_name = sys.argv[1]
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print("{} is not installed.".format(package_name))
    else:
        #print(importlib.util.find_spec(package_name).origin)
        package = __import__(package_name)
        if hasattr(package, '__version__'):
        	print("{}=={}".format(package_name, package.__version__))
        else:
            for i in installed_packages:
                if (i.key == package_name):
                    print("{}=={}".format(i.key, i.version))
else:
    print("Specify a python package.")
