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

dir = os.path.split(sys.argv[0])[0]
if bool(dir):
    dir += '\\*.py'
else:
    dir = '*.py'

def enumerate_scripts(list):
    i = 0
    while i < len(list):
        line = ''
        for j in range(step):
            k = i + j
            if k < len(list):
                line += '%-20s' %(list[k])
            else:
                break
        i += step
        print(line)
    print('%s files are found.\n' %(len(list)))

list_py = []
list_exe = []
for file in glob.glob(dir):        
    filename = os.path.basename(file)
    list_py.append(filename)
    file = os.path.splitext(file)[0] + '.exe'
    if os.path.exists(file):
        filename = os.path.basename(file)
        list_exe.append(filename)
        
enumerate_scripts(list_py)
enumerate_scripts(list_exe)