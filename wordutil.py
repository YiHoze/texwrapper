import os, sys, argparse, glob, subprocess, re

parser = argparse.ArgumentParser(
    description='Count or extract words from text files. This script can process PDF files if TeX Live is installed.'
)

parser.add_argument(
    'files',
    type=str,
    nargs='+',
    help='Specify text files.'
)
parser.add_argument(
    '-e',
    dest = 'extract',
    action = 'store_true',
    default = False,
    help = 'Extract words.'
)
parser.add_argument(
    '-k',
    dest = 'keep',
    action = 'store_true',
    default = False,
    help = 'keep numbers and TeX macros when extracting words.'
)
parser.add_argument(
    '-s',
    dest = 'suffix',
    default = 'extracted',
    help = 'Specify a suffix for output. (default: foo_extracted.txt)'
)
args = parser.parse_args()

try:
    cmd = 'pdftotext -v'
    subprocess.check_call(cmd)
    pdftotext = True
except OSError:
    print('pdftotext.exe is not found, so PDF files cannot be processed.')
    pdftotext = False

reserved_patterns = [
    r'\\[^a-zA-Z]', 
    r'\\[a-zA-Z*^|+]+',
    r'\\begin\{.+?\}[*^|+]*', 
    r'\\end\{.+?\}[*^|+]*',
    r'\w+=',
    r'\w*\d\w*'
]

# Spaces are not counted as a character.
def count_words(afile):
    lines, chars, words = 0, 0, 0
    f = open(afile, mode='r', encoding='utf-8')
    for line in f.readlines():
        lines += 1
        chars += len(line.replace(' ', '')) 
        this = line.split(None)
        words += len(this)
    f.close()
    msg = '%s\n Lines: %d\n Words: %d\n Characters: %d\n' % (afile, lines, words, chars)
    print(msg) 

def extract_words(afile):
    filename = os.path.basename(afile)
    basename, ext = os.path.splitext(filename)
    output = '%s_%s%s' %(basename, args.suffix, ext)
    if os.path.exists(output):
        answer = input('%s alread exists. Are you sure to overwrite it? [y/N] ' %(output))
        if answer.lower() == 'y':
            os.remove(output)
        else:
            return
    with open(afile, mode='r', encoding='utf-8') as f:
        content = f.read()
    if not args.keep: 
        for i in range(len(reserved_patterns)):
            content = re.sub(reserved_patterns[i], '', content) # remove numbers and tex macros
    p = re.compile('\w+')
    extracted = p.findall(content)
    extracted = set(extracted)
    content = '\n'.join(sorted(extracted))
    with open(output, mode='w', encoding='utf-8') as f:
        f.write(content)
    cmd = 'powershell -command open.py %s' %(output)
    os.system(cmd)

def check_and_convert(afile):
    filename = os.path.basename(afile)
    basename, ext = os.path.splitext(filename)
    if ext.lower() == '.pdf':
        cmd = 'pdftotext -nopgbrk -raw -enc UTF-8 %s' % (afile)
        os.system(cmd)
        filename = basename + '.txt'
    return(filename)

for fnpattern in args.files:
    for afile in glob.glob(fnpattern):
        afile = check_and_convert(afile)
        count_words(afile)
        if args.extract:
            extract_words(afile)