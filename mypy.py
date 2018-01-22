import os, sys, glob, argparse

try:
    dir_called = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    dir_called = False
if dir_called is False:
    dir_called = os.path.dirname(sys.argv[0])

pylist = os.path.join(dir_called, 'py.list')
dir_called = os.path.join(dir_called, '*.py')

parser = argparse.ArgumentParser(
    description = 'Count your python scripts.'
)
parser.add_argument(
    'columns',
    type = int,
    nargs = '*',
    help = 'specify the number of columns (default: 3)'
)
parser.add_argument(
    '-o',
    dest = 'output',
    default = pylist,
    help = 'specify a filename for output (default: py.list)'
)
args = parser.parse_args()

if bool(args.columns):
    step = args.columns[0]
else:
    step = 3 

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
with open(args.output, mode='w') as f:
    for afile in glob.glob(dir_called):
        filename = os.path.basename(afile)
        list_py.append(filename)
        f.write('%s\n' %(filename))
        afile = os.path.splitext(afile)[0] + '.exe'        
        if os.path.exists(afile):
            filename = os.path.basename(afile)
            list_exe.append(filename)
        
enumerate_scripts(list_py)
enumerate_scripts(list_exe)