import os, sys, glob, argparse, re

parser = argparse.ArgumentParser(
    description = 'Extract words from a text file.'
)
parser.add_argument(
    'txt',
    nargs = 1,
    help ='specify a text file'
)
parser.add_argument(
    '-k',
    dest = 'keep',
    action = 'store_true',
    default = False,
    help = 'keep numbers and tex macros'
)
parser.add_argument(
    '-o',
    dest = 'output',
    default = None,
    help = 'specify a filename for output (default: foo_extracted.txt)'
)
args = parser.parse_args()

if not os.path.exists(args.txt[0]):
    print('%s is not extracted' %(args.txt[0]))
    sys.exit()

if args.output is None:
    args.output = os.path.splitext(args.txt[0])[0] + '_extracted.txt'

if os.path.exists(args.output):
    answer = input('%s alread exists. Are you sure to overwrite it? [y/N] ' %(args.output))
    if answer.lower() == 'y':
        os.remove(args.output)
    else:
        sys.exit()

reserved_patterns = [
    r'\\[^a-zA-Z]', 
    r'\\[a-zA-Z*^|+]+',
    r'\\begin\{.+?\}[*^|+]*', 
    r'\\end\{.+?\}[*^|+]*',
    r'\w+=',
    r'\w*\d\w*'
]

with open(args.txt[0], mode='r', encoding='utf-8') as f:
    content = f.read()

if not args.keep:
    for i in range(len(reserved_patterns)):
        content = re.sub(reserved_patterns[i], '', content)

p = re.compile('\w+')
extracted = p.findall(content)
extracted = set(extracted)
output = '\n'.join(sorted(extracted))

with open(args.output, mode='w', encoding='utf-8') as f:
    f.write(output)

os.system('open.exe %s' %(args.output))
