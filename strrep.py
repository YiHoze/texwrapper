import os, sys, glob, argparse, configparser, csv, re

# Read the initiation file to get the tab-separated file for string replacement.
try:
    inipath = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    inipath = False
if inipath is False:
    inipath = os.path.dirname(sys.argv[0])
ini = os.path.join(inipath, 'docenv.ini')
if os.path.exists(ini):
    config = configparser.ConfigParser()
    config.read(ini)
    try:
        pattern = config.get('String Replacement', 'file')
    except:
        print('Make sure to have docenv.ini set properly.')
        sys.exit()
else:
    print('Docenv.ini is not found. Set the DOCENV environment variable to the directory containing docenv.ini.')
    sys.exit() 

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
    help = 'Specify another string pattern file to use it.'
)
args = parser.parse_args()

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