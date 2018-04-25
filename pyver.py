import sys, pip, pkg_resources, imp, importlib.util

if len(sys.argv) > 1:
    package_name = sys.argv[1]
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print("{} is not installed.".format(package_name))
    else:
        package = __import__(package_name)
        if hasattr(package, '__version__'):
        	print("{}=={}".format(package_name, package.__version__))
        else:
            imp.reload(pkg_resources)
            installed_packages = [(i.key, i.version) for i in pkg_resources.find_distributions(sys.path[5])]  
            for i in installed_packages:
                if (i.key == package_name):
                    print("{}=={}".format(i.key, i.version))
else:
    print("Specify a python package.")
