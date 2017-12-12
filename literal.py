import os, sys, glob, argparse, configparser, csv, re

# Read the initiation file to get the tab-separated file for string replacement.
ini = os.path.split(sys.argv[0])[0] 
if bool(ini):
    inipath = ini
    ini += '\\docenv.ini'    
else:
    ini = 'docenv.ini'
config = configparser.ConfigParser()
if os.path.exists(ini):
    config.read(ini)
    try:
        literal = config.get('Literal', 'file')
    except:
        literal = 'strpattern.tsv'
else:
    literal = 'strpattern.tsv'

if bool(inipath):
    literal = inipath + '\\' + literal

if not os.path.exists(literal):
    print('literal.tsv is not found.')
    sys.exit()

parser = argparse.ArgumentParser(
    description = 'Make long strings in tex files breakable.'
)
parser.add_argument(
    'tex',
    nargs = '+',
    help = 'Specify one or more TeX files.'
)
args = parser.parse_args()

tmp = 't@mp.t@mp'
if os.path.exists(tmp):
    os.remove(tmp)

def literal_replace(file):
    with open(file, mode='r', encoding='utf-8') as f:
        content = f.read()
    with open(literal, mode='r', encoding='utf-8') as tsv:
        reader = csv.reader(tsv, delimiter='\t')
        for row in reader:            
            content = re.sub(row[0], row[1], content)        
    with open(tmp, mode='w', encoding='utf-8') as f:
       f.write(content)
    os.remove(file)
    os.rename(tmp, file)

for files in args.tex:
    for file in glob.glob(files):
        literal_replace(file)