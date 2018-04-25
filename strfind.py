import os, sys, glob, argparse, csv, re, codecs

parser = argparse.ArgumentParser(
    description = 'Search a text file to find or replace some strings with others.'
)
parser.add_argument(
    'files',
    nargs = '+',
    help = 'specify one or more text files'
)
parser.add_argument(
    '-t',
    dest = 'target',
    default = None,
    help = 'specify a string to find'

)
parser.add_argument(
    '-s',
    dest = 'substitute',
    default = None,
    help = 'specify a string with which to replace found strings'

)
parser.add_argument(
    '-b',
    dest = 'backup',
    action = 'store_true',
    default = False,
    help = 'Make a backup copy'
)
parser.add_argument(
    '-p',
    dest = 'pattern',
    default = None,
    help = 'specify a file that includes substitution patterns. (foo.tsv)'
)
parser.add_argument(
    '-r',
    dest = 'recursive',
    action = 'store_true',
    default = False,
    help = 'process ones in all subdirectories'
)
args = parser.parse_args()

def get_subdirs(fnpattern):
    curdir = os.path.dirname(fnpattern)
    if curdir == '':
        curdir = '.'
    return([x[0] for x in os.walk(curdir)])

def find_to_display():
    for fnpattern in args.files:
        for afile in glob.glob(fnpattern):
            find_to_display_sub(afile)
        if args.recursive:
            basename = os.path.basename(fnpattern)
            subdirs = get_subdirs(fnpattern)
            for subdir in subdirs:   
                subfile = os.path.join(subdir, basename)
                for afile in glob.glob(subfile):
                    find_to_display_sub(afile)

def find_to_display_sub(afile):
    print(afile)    
    try:
        with open(afile, mode='r', encoding='utf-8') as f:        
                for num, line in enumerate(f):                
                    if re.search(args.target, line):
                        print('%5d:\t%s' %(num, line.replace('\n', ' ')))
    except:
        print('is not encoded in UTF-8.')
        return

def replace_to_write():    
    for fnpattern in args.files:
        for afile in glob.glob(fnpattern):
            replace_to_write_sub(afile)
        if args.recursive:            
            basename = os.path.basename(fnpattern)
            subdirs = get_subdirs(fnpattern)
            for subdir in subdirs:   
                subfile = os.path.join(subdir, basename)
                for afile in glob.glob(subfile):
                    replace_to_write_sub(afile)  

def replace_to_write_sub(afile):
    tmp = 't@mp.t@mp'
    try:
        with open(afile, mode='r', encoding='utf-8') as f:
            content = f.read() 
    except:
        print('%s is not encoded in UTF-8.' %(afile))
        return        
    if args.pattern is None:
        content = re.sub(args.target, args.substitute, content)
    else:
        with open(args.pattern, mode='r', encoding='utf-8') as tsv:
            reader = csv.reader(tsv, delimiter='\t')
            for row in reader:            
                content = re.sub(row[0], row[1], content) 
    with open(tmp, mode='w', encoding='utf-8') as f:
        f.write(content)
    if args.backup:
        backup = os.path.splitext(afile)[0] + '_bak' + os.path.splitext(afile)[1]
        if os.path.exists(backup):
            os.remove(backup)
        os.rename(afile, backup)
    if os.path.exists(afile):
        os.remove(afile)
    os.rename(tmp, afile)

if args.pattern is None:        
    if args.target is None:
        parser.print_help()
        sys.exit()
    elif args.substitute is None:
        find_to_display()
    else:
        replace_to_write()
else:
    if os.path.exists(args.pattern):
        replace_to_write()
    else:
        print('%s is not found.' %(args.pattern))