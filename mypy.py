import os, sys, glob, argparse

parser = argparse.ArgumentParser(
    description = 'Count your python scripts.'
)
parser.add_argument(
    'columns',
    type = int,
    nargs = '*',
    help = 'Specify the number of columns. (default: 3)'
)
args = parser.parse_args()

if bool(args.columns):
    step = args.columns[0]
else:
    step = 3 

bindir = os.path.split(sys.argv[0])[0]
if bool(bindir):
    bindir += '\\*.py'
else:
    bindir = '*.py'

def enumerate_scripts(alist):
    i = 0
    while i < len(alist):
        line = ''
        for j in range(step):
            k = i + j
            if k < len(alist):
                line += '%-20s' %(alist[k])
            else:
                break
        i += step
        print(line)
    print('%s files are found.\n' %(len(alist)))

list_py = []
list_exe = []
for afile in glob.glob(bindir):
    filename = os.path.basename(afile)
    list_py.append(filename)
    afile = os.path.splitext(afile)[0] + '.exe'
    if os.path.exists(afile):
        filename = os.path.basename(afile)
        list_exe.append(filename)
        
enumerate_scripts(list_py)
enumerate_scripts(list_exe)