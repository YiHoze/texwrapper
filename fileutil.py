import os, sys, shutil, glob, argparse, datetime, re

now = datetime.datetime.now()
today = now.strftime('_%Y-%m-%d')

parser = argparse.ArgumentParser(
    description = 'Append a date or suffix to filenames'
)

parser.add_argument(
    'files',
    nargs = '+',
    help = 'Specify one or more files'
)
parser.add_argument(
    '-s',
    dest = 'suffix',
    default = today,
    help = 'Specify a date or suffix. The dafult is the current date.'
)
parser.add_argument(
    '-r',
    dest = 'remove',
    action = 'store_true',
    default = False,
    help = 'Remove a suffix from filenames.'
)
parser.add_argument(
    '-u',
    dest = 'uppercase',
    action = 'store_true',
    default = False,
    help = 'Rename files to uppercase.'
)
parser.add_argument(
    '-l',
    dest = 'lowercase',
    action = 'store_true',
    default = False,
    help = 'Rename files to lowercase.'
)
parser.add_argument(
    '-c',
    dest = 'copy',
    action = 'store_true',
    default = False,
    help = 'Copy fiels from multiple folders to one folder.'
)
parser.add_argument(
    '-t',
    dest = 'target_folder',
    help = 'Specify your target folder.'
)
args = parser.parse_args()

def RenameUppercase():
    for fnpattern in args.files:
        for afile in glob.glob(fnpattern):
            filename = os.path.splitext(afile)
            newname = filename[0].upper() +  filename[1].upper()            
            os.rename(afile, newname)

def RenameLowercase():
    for fnpattern in args.files:
        for afile in glob.glob(fnpattern):
            filename = os.path.splitext(afile)
            newname = filename[0].lower() +  filename[1].lower()            
            os.rename(afile, newname)

def AppendSuffix():
    for fnpattern in args.files:
        for afile in glob.glob(fnpattern):
            filename = os.path.splitext(afile)
            newname = filename[0] + args.suffix + filename[1]            
            os.rename(afile, newname)

def RemoveSuffix():
    for fnpattern in args.files:
        for afile in glob.glob(fnpattern):
            newname = re.sub(args.suffix, '', afile)
            os.rename(afile, newname)

def get_subdirs(fnpattern):
    curdir = os.path.dirname(fnpattern)
    if curdir == '':
        curdir = '.'
    return([x[0] for x in os.walk(curdir)])

def CopyIntoOne():
    if not os.path.exists(args.target_folder):
        answer = input('The %s folder is not found. If you want to create it, Enter Y. ' % (args.target_folder))
        if (answer.lower() == 'y'):
            os.mkdir(args.target_folder)
        else:
            sys.exit(False)
    for fnpattern in args.files:
        basename = os.path.basename(fnpattern)
        subdirs = get_subdirs(fnpattern)
        for subdir in subdirs:   
            subfile = os.path.join(subdir, basename)
            for afile in glob.glob(subfile):
                shutil.copy(afile, args.target_folder)

if args.uppercase:
    RenameUppercase()
elif args.lowercase:
    RenameLowercase()
elif args.remove:
    RemoveSuffix()
elif args.copy:
    CopyIntoOne()
else:
    AppendSuffix()    