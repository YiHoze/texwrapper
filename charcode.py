import os, sys, argparse
import unicodedata

parser = argparse.ArgumentParser(
    description = 'View codes of characters in a text file encoded in UTF-8.'
)
parser.add_argument(
    'file',
    nargs = 1,
    help = 'specify a text file'
)
parser.add_argument(
    '-o',
    dest = 'output',
    action = 'store_true',
    default = False,
    help = 'write the output to a file (foo_unicode.txt)'
)
args = parser.parse_args()

def display_unicode(string):
    codes = ''
    for i, c in enumerate(string):                        
        if (c != '\n') and (c != ' '):
            codes += '%s\tU+%04X\t%s\n' %(c, ord(c), unicodedata.name(c).lower())
    return(codes)

if not os.path.exists(args.file[0]):
    print('%s is not found.' %(args.file[0]))
    sys.exit()
if args.output:
    filename = os.path.splitext(args.file[0])[0] + "_unicode.txt"
    outfile = open(filename, mode='w', encoding='utf-8')
infile = open(args.file[0], mode='r', encoding='utf-8')
for line in infile.readlines():
    codes = display_unicode(line)
    if args.output:
        outfile.write(codes)
    else:
        print(codes)
infile.close()
if args.output:
    outfile.close()
    os.system('open.exe %s' %(filename))