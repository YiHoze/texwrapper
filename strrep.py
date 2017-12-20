import os, sys, glob, argparse, configparser, csv, re

# Read the initiation file to get the tab-separated file for string replacement.
ini = os.path.split(sys.argv[0])[0] 
if bool(ini):
    inipath = ini
    ini += '\\docenv.ini'    
else: # in case this source code is called by Python when the terminal's current directory is that which contains this script.
    inipath = '.'
    ini = 'docenv.ini'
config = configparser.ConfigParser()
if os.path.exists(ini):
    config.read(ini)
    try:
        pattern = config.get('String Replacement', 'file')
    except:
        pattern = 'strpattern.tsv'
else:
    pattern = 'strpattern.tsv'

if not os.path.exists(pattern):
    pattern = os.path.join(inipath, pattern)

parser = argparse.ArgumentParser(
    description = 'Replace some strings with others. strpattern.tsv is used by default for string replacement.'
)
parser.add_argument(
    'tex',
    nargs = '+',
    help = 'Specify one or more TeX files.'
)
parser.add_argument(
    '-p',
    dest = 'pattern',
    default = pattern,
    help = 'Specify a string pattern file.'
)
args = parser.parse_args()

pattern 
if not os.path.exists(args.pattern):
    print('%s is not found.' %(args.pattern))
    sys.exit()

tmp = 't@mp.t@mp'
if os.path.exists(tmp):
    os.remove(tmp)

def strpattern_replace(tex):
    with open(tex, mode='r', encoding='utf-8') as f:
        content = f.read()
    with open(args.pattern, mode='r', encoding='utf-8') as tsv:
        reader = csv.reader(tsv, delimiter='\t')
        for row in reader:            
            content = re.sub(row[0], row[1], content)            
    with open(tmp, mode='w', encoding='utf-8') as f:
       f.write(content)
    os.remove(tex)
    os.rename(tmp, tex)

for fnpattern in args.tex:
    for tex in glob.glob(fnpattern):
        strpattern_replace(tex)