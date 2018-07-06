import os, sys, glob, argparse, re

# sys.path.append(...)
# from foo import *

parser = argparse.ArgumentParser(
    description='Convert a TeX file to PDF using XeLaTeX or LuaLaTeX.'
)
parser.add_argument(
    'tex',
    type=str,
    nargs='?',
    help='Specify a TeX file.'
)
parser.add_argument(
    '-n',
    dest='no_compile',
    action='store_true',
    default=False,
    help='Do not compile.'
)
parser.add_argument(
    '-b',
    dest='batch_mode',
    action='store_true',
    default=False,
    help='LaTeX does not halt even with syntax errors.'
)
parser.add_argument(
    '-s',
    dest='shell_escape',
    action='store_true',
    default=False,
    help='Allow an external program to run during a XeLaTeX run.'
)
parser.add_argument(
    '-w',
    dest='twice_compile',
    action='store_true',
    default=False,
    help='Compile twice.'
)
parser.add_argument(
    '-f',
    dest='full_compile',
    action='store_true',
    default=False,
    help='Compile fully.'
)
parser.add_argument(
    '-i',
    dest='index_sort',
    action='store_true',
    default=False,
    help='Sort index using TeXindy.'
)
parser.add_argument(
    '-l',
    dest='lualatex',
    action='store_true',
    default=False,
    help='Use LuaLaTeX instead of XeLaTeX.'
)
parser.add_argument(
    '-lang',
    dest='language',
    default='korean',
    help='Specify a language to sort index entries. For example, \"german\" or \"ger\" for German. The default is \"korean\".'
)
parser.add_argument(
    '-k',
    dest='komkindex',
    action='store_true',
    default=False,
    help='Use komkindex instead of TeXindy.'
)
parser.add_argument(
    '-ist',
    dest='index_style',
    default='kotex',
    help='Specify an index style for komkindex. The dafault is kotex.ist.'
)
parser.add_argument(
    '-a',
    dest='keep_aux',
    action='store_true',
    default=False,
    help='After a full compilation (-f), auxiliary files are deleted. Use this option to keep them.'    
)
parser.add_argument(
    '-m',
    dest='bookmark_index',
    action='store_true',
    default=False,
    help='Bookmark all index entries. This option is available only with full compilation (-f). This feature does not support komkindex.'
)
parser.add_argument(
    '-p',
    dest='bookmark_python',
    action='store_true',
    default=False,
    help='Bookmark index entries which are Python functions extracted from docstrings. This option is available only with full compilation (-f).'
)
parser.add_argument(
    '-c',
    dest='clean_aux',
    action='store_true',
    default=False,
    help='Remove auxiliary files after compilation.'
)
parser.add_argument(
    '-fin',
    dest='finalizer',
    action='store_true',
    default=False,
    help='Find \\FinalizerOff to replace it with \\FinalizerOn in the tex file.'    
)
parser.add_argument(
    '-d',
    dest='draft',
    action='store_true',
    default=False,
    help='Find \\FinalizerON to replace it with \\FinalizerOff in the tex file.'    
)
args = parser.parse_args()

# In case of a wrong filename extension
if args.tex is not None:
    filename = os.path.basename(args.tex)
    basename = os.path.splitext(filename)[0]
    tex = basename + '.tex'
    idx = basename + '.idx'
    ind = basename + '.ind'
    if not os.path.exists(tex):
        msg = '%s is not found.' % (tex)
        print(msg)
        sys.exit(False)

if args.lualatex:
    compiler = 'lualatex.exe'
else:
    compiler = 'xelatex.exe'

# Compile mode
if args.batch_mode or args.full_compile:
    compile_mode = '-interaction=batchmode'
else:
    compile_mode = '-synctex=1'
if args.shell_escape:
    compile_mode += '-shell-escape -8bit'

# language by which to sort index
index_modules = {
  'eng': 'lang/english/utf8-lang ',
  'fre': 'lang/french/utf8-lang ',
  'ger': 'lang/german/din5007-utf8-lang ',
  'ita': 'lang/italian/utf8-lang ',
  'kor': 'lang/korean/utf8-lang ',
  'rus': 'lang/russian/utf8-lang ',
  'spa': 'lang/spanish/modern-utf8-lang ',
}
try:
    ind_mod = index_modules[args.language[:3].lower()]
except:
    ind_mod = index_modules['eng']

# functions
def compile_once():
    os.system(cmd_tex)

def compile_twice():
    os.system(cmd_tex)
    if args.index_sort:
        sort_index()
    else:
        os.system(cmd_tex)

def compile_fully():
    os.system(cmd_tex)
    os.system(cmd_tex)
    sort_index()    
    os.system(cmd_tex)
    if not args.keep_aux:
        clean_aux()

def sort_index():
    if not os.path.exists(idx):
        print('%s is not found' % (idx))
        return
    if args.komkindex:        
        cmd = 'komkindex.exe -s %s %s' %(args.index_style, idx)
    else:
        cmd = 'texindy.exe --module %s %s' %(ind_mod, idx) 
    os.system(cmd)    
    if args.bookmark_index or args.bookmark_python:
        bookmark_index()
    if not args.no_compile:
        os.system(cmd_tex)

def bookmark_index():

    if not os.path.exists(ind):
        print('%s is not found' % (ind))
        return
    tmp = 't@mp.ind'
    if os.path.exists(tmp):
        os.remove(tmp)
    with open(tmp, mode='w', encoding='utf-8') as new_file, open(ind, mode='r', encoding='utf-8') as old_file:
        if args.bookmark_python:
            for line in old_file.readlines():
                new_file.write(bookmark_index_item(line, r'\\item (.+?)\(\)'))
        else:
            for line in old_file.readlines():
                new_file.write(bookmark_index_item(line, r'\\item (.+?),'))         
    os.remove(ind)
    os.rename(tmp, ind)

def bookmark_index_item(line, pattern):
    entry = re.search(pattern, line)
    if entry: 
        page = re.findall(r'\\hyperpage\{(\d+)\}', line)
        append = ''
        for i in range(len(page)):
            append += '\t\\bookmark[level=2, page=%s]{%s}\n' %(page[i], entry.group(1))                    
        line += append
    return(line)  

def clean_aux():
    extensions = {"aux", "bbl", "blg", "idx", "ilg", "ind", "loe", "lof", "log", "lop", "loq", "lot", "minted*", "mw", "nav", "out", "synctex*", "snm", "toc*", "upa", "upb", "vrb"}
    for ext in extensions:
        fnpattern = '*.' + ext
        for afile in glob.glob(fnpattern):
            os.remove(afile)

def finalizer():
    with open(tex, mode='r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub("\\\\FinalizerOff", "\\\\FinalizerOn", content)
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)

def draft():
    with open(tex, mode='r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub("\\\\FinalizerOn", "\\\\FinalizerOff", content)
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)


if args.finalizer:
    finalizer()
if args.draft:
    draft()

if not args.no_compile:
    if args.tex is not None:
        cmd_tex = '%s %s %s' %(compiler, compile_mode, tex)
        if args.full_compile:
            compile_fully()
        elif args.twice_compile:
            compile_twice()
        else:
            compile_once()

#if args.no_compile:
if args.tex is not None:
    if args.index_sort or args.komkindex:
        sort_index()
    elif args.bookmark_index or args.bookmark_python:
        bookmark_index()

if args.clean_aux:
    clean_aux()    