import os, sys, glob, argparse

try:
    dir_called = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    dir_called = False
if dir_called is False:
    dir_called = os.path.dirname(sys.argv[0])

dir_called = os.path.join(dir_called, '*.py')

parser = argparse.ArgumentParser(
    description = 'Count my python scripts.'
)
parser.add_argument(
    'columns',
    nargs = '?',
    help = 'Specify the number of columns (default: 3)'
)
args = parser.parse_args()

if args.columns is None:
    step = 3    
else:
    step = int(args.columns)

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
for afile in glob.glob(dir_called):
    filename = os.path.basename(afile)
    list_py.append(filename)
enumerate_scripts(list_py)