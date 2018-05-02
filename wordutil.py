import os, sys, argparse, glob, subprocess, re, unicodedata

parser = argparse.ArgumentParser(
    description='With this script, you can 1) count or extract words from a text file; 2) view codes of characters in a file encoded in UTF-8; 3) extract tex macros from a tex file. This script can process PDF files if TeX Live is installed. Be aware that the output file is encoded in EUC-KR as for extracted tex macros.'
)

parser.add_argument(
    'files',
    type=str,
    nargs='+',
    help='Specify one or more text files.'
)
parser.add_argument(
    '-u',
    dest = 'unicode',
    action = 'store_true',
    default = False,
    help = 'View character codes in Unicode.'
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
    help = 'Keep numbers and TeX macros when extracting words.'
)
parser.add_argument(
    '-t',
    dest = 'tex',
    action = 'store_true',
    default = False,
    help = 'Extract TeX macros.'
)
parser.add_argument(
    '-tor',
    dest = 'tortoise',
    action = 'store_true',
    default = False,
    help = 'Prepend the Tortoise Tagger syntax to the output for reference. This is available only with the -t option.'
)
parser.add_argument(
    '-s',
    dest = 'suffix',    
    help = 'Specify a suffix for output. The default varies by option.'
)
args = parser.parse_args()

try:
    cmd = 'pdftotext -v'
    subprocess.check_call(cmd)
    pdftotext = True
except OSError:
    print('pdftotext.exe is not found, so PDF files cannot be processed.')
    pdftotext = False

if args.suffix is None:
    if args.unicode:
        args.suffix = 'unicode'
    elif args.tex:
        args.suffix = 'picked'
    else:
        args.suffix = 'extracted'

if args.tex:
    reserved_patterns = [
        r'\\[^a-zA-Z]', 
        r'\\[a-zA-Z*^|+]+',
        r'\\begin(\{.+?\}[*^|+]*)', 
        r'(\w+=)'
    ]
else:
    reserved_patterns = [
        r'\\[^a-zA-Z]', 
        r'\\[a-zA-Z*^|+]+',
        r'\\begin\{.+?\}[*^|+]*', 
        r'\\end\{.+?\}[*^|+]*',
        r'\w+=',
        r'\w*\d\w*'
    ]

tortoise = """
~~~FindAsIs
~~~WriteAsIs
~~~WC-OFF
\이 이
\가 가
\을 을
\를 를
\은 은
\는 는
\와 와
\과 과
\로 로
\으로 으로
\라 라
\이라 이라
~~~FindAsIs
~~~WriteInternal
~~~WC-ON
~~~FindAsIs
~~~WriteInternal
~~~WC-OFF
{
}
[
]
&
"""
# Spaces are not counted as a character.
def check_to_remove(afile):
    if os.path.exists(afile):
        answer = input('%s alread exists. Are you sure to overwrite it? [y/N] ' %(afile))
        if answer.lower() == 'y':
            os.remove(afile)
            return True
        else:
            return False
    else:
        return True

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
    basename = os.path.splitext(afile)[0]
    output = '%s_%s.txt' %(basename, args.suffix)
    if check_to_remove(output) is False:
        return    
    with open(afile, mode='r', encoding='utf-8') as f:
        content = f.read()
    # remove numbers and tex macros
    if not args.keep: 
        for i in range(len(reserved_patterns)):
            content = re.sub(reserved_patterns[i], '', content) 
    p = re.compile('\w+')
    extracted = p.findall(content)
    extracted = set(extracted)
    content = '\n'.join(sorted(extracted))
    with open(output, mode='w', encoding='utf-8') as f:
        f.write(content)
    cmd = 'powershell -command open.py %s' %(output)
    os.system(cmd)

def display_unicode(string):
    codes = ''
    for i, c in enumerate(string):                        
        if (c != '\n') and (c != ' '):
            codes += '%s\tU+%04X\t%s\n' %(c, ord(c), unicodedata.name(c).lower())
    return codes

def get_unicode(afile):
    basename = os.path.splitext(afile)[0]
    output = '%s_%s.txt' %(basename, args.suffix)
    if check_to_remove(output) is False:
        return    
    with open(afile, mode='r', encoding='utf-8') as infile, open(output, mode='w', encoding='utf-8') as outfile:
        for line in infile.readlines():
            codes = display_unicode(line)
            outfile.write(codes)
    cmd = 'powershell -command open.py %s' %(output)
    os.system(cmd)

def check_to_convert(afile):
    filename = os.path.basename(afile)
    basename, ext = os.path.splitext(filename)    
    if ext.lower() == '.pdf':
        if pdftotext is True:
            filename = basename + '.txt'
            if check_to_remove(filename) is False:
                return    
            else:
                cmd = 'pdftotext -nopgbrk -raw -enc UTF-8 %s' % (afile)
                os.system(cmd)            
                return filename
        else:
            return
    else:
        return filename

def pick_tex_macro(afile):
    basename = os.path.splitext(afile)[0]
    output = '%s_%s.txt' %(basename, args.suffix)
    if check_to_remove(output) is False:
        return
    found = []
    with open(afile, mode='r', encoding='utf-8') as f:
        content = f.read()
    # pick tex macros and keys
    for i in range(len(reserved_patterns)):
        p = re.compile(reserved_patterns[i])
        found += p.findall(content)
    # remove duplicates and sort
    found = set(found)
    macros = '\n'.join(sorted(found, key=str.lower))
    if args.tortoise:
        macros = tortoise + macros
    with open(output, mode='w', encoding='euc-kr') as f:
        f.write(macros)
    cmd = 'powershell -command open.py %s' %(output)
    os.system(cmd)

for fnpattern in args.files:
    for afile in glob.glob(fnpattern):
        afile = check_to_convert(afile)
        if afile is not None:
            if args.extract:
                extract_words(afile)
            elif args.unicode:
                get_unicode(afile)
            elif args.tex:
                pick_tex_macro(afile)
            else:
                count_words(afile)