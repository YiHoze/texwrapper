import os, sys, glob, argparse, subprocess

parser = argparse.ArgumentParser(
    description = 'Convert EPS files to PDF or the other way using epstopdf and pdftops of TeX Live.'
)
parser.add_argument(
    'files',
    nargs = '+',
    help = 'specify one or more EPS or PDF files'
)
parser.add_argument(
    '-s',
    dest = 'recursive',
    action = 'store_true',
    default = False,
    help = 'process ones in all subdirectories'
)
parser.add_argument(
    '-c',
    dest = 'contrary',
    action = 'store_true',
    default = False,
    help = 'covert PDF files to EPS'
)
args = parser.parse_args()

try:
    subprocess.check_call('epstopdf.exe --version')
except OSError:
    print("Make sure TeX Live is included in PATH.")    
    sys.exit(False)

def get_subdirs(fnpattern):
    curdir = os.path.dirname(fnpattern)
    if curdir == '':
        curdir = '.'
    return([x[0] for x in os.walk(curdir)])

def eps_to_pdf(afile):
    if args.contrary:
        os.system('pdftops -eps %s' %(afile))
    else:
        os.system('epstopdf.exe %s' %(afile))

cnt = 0
for fnpattern in args.files:
    ext = os.path.splitext(fnpattern)[1]
    if args.contrary:
        if ext.lower() != '.pdf':
            print('Specify PDF files.')
            continue
    else:
        if ext.lower() != '.eps':
            print('Specify EPS files.')
            continue
    for afile in glob.glob(fnpattern):
        eps_to_pdf(afile)
        cnt += 1        
    if args.recursive:
        basename = os.path.basename(fnpattern)        
        subdirs = get_subdirs(fnpattern)
        for subdir in subdirs:
            subfile = os.path.join(subdir, basename)
            for afile in glob.glob(subfile):
                eps_to_pdf(afile)
                cnt += 1
print('%d file(s) have been converted.' %(cnt))