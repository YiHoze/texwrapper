import os, sys, glob, argparse

# Get arguments
parser = argparse.ArgumentParser(
    description = 'Build python scripts.'
)
parser.add_argument(
    'files',
    type=str,
    nargs='*',
    help='If no python file is specified, every python file listed in py.list is to be build.'
)
parser.add_argument(
    '-l',
    dest='pylist',
    type=str,
    default='py.list',
    help='Specify a list file that enumerates python files to use it instead of py.list'
)
args = parser.parse_args()

# Collect python scripts to build.
list_py = []
if not bool(args.files):
    f = open(args.pylist, mode='r', encoding='utf-8')
    lines = f.readlines()
    f.close()    
    for line in lines:
        list_py.append(line.replace('\n', ''))
else:
    for fnpattern in args.files:
        for afile in glob.glob(fnpattern):
            list_py.append(afile)

# compile to binary executable
for py in list_py:
    if py == 'pybuild.py':
        continue
    cmd = 'pyinstaller --onefile --specpath .\\dist %s' % (py)
    try:
        os.system(cmd)
    except OSError:
        msg = 'Make sure %s is well coded.' % (py)
        print(msg)

for py in list_py:
    if py == 'pybuild.py':
        continue
    filename = os.path.splitext(py)[0]    
    src = 'dist\\' + filename + '.exe'
    cmd = 'copy %s .' %(src)
    os.system(cmd)    