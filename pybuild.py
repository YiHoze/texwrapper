import os, sys, glob, argparse, shutil

# Get arguments
parser = argparse.ArgumentParser(
    description = 'Build python scripts.'
)
parser.add_argument(
    'files',
    type=str,
    nargs='*',
    help='If no python file is specified, every python file listed in the pylist.txt is to be build.'
)
parser.add_argument(
    '-l',
    dest='list',
    type=str,
    default='pylist.txt',
    help='Specify a list file that enumerates python files to use it instead of pylist.txt.'
)
parser.add_argument(
    '-k',
    dest = 'keep_spec',
    action = 'store_true',
    default = False,
    help = 'Keep spec files.'
)
args = parser.parse_args()

# Collect python scripts to build.
pys = []
if not bool(args.files):
    f = open(args.list, mode='r', encoding='utf-8')
    lines = f.readlines()
    f.close()    
    for line in lines:
        pys.append(line.replace('\n', ''))
else:
    for pattern in args.files:
        for file in glob.glob(pattern):
            pys.append(file)

for py in pys:
    cmd = 'pyinstaller --onefile %s' % (py)
    try:
        os.system(cmd)
    except OSError:
        msg = 'Make sure %s is well coded.' % (py)
        print(msg)

for py in pys:
    filename = os.path.splitext(py)[0]
    trg = filename + '.exe'
    src = 'dist\\' + trg    
    shutil.copyfile(src, trg)
    if not args.keep_spec:
        src = filename + '.spec'    
        if os.path.exists(src):
            os.remove(src)
    