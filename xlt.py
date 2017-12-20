import os, glob, argparse, subprocess
# import configparser

parser = argparse.ArgumentParser(
    description='Convert a TeX file to PDF using XeLaTeX.'
)
parser.add_argument(
    'tex',
    type=str,
    nargs=1,
    help='Specify a TeX file.'
)
parser.add_argument(
    '-b',
    dest='BatchMode',
    action='store_true',
    default=False,
    help='XeLaTeX does not halt even with syntax errors.'
)
parser.add_argument(
    '-s',
    dest='ShellEscape',
    action='store_true',
    default=False,
    help='Allow an external program to run during a XeLaTeX run.'
)
parser.add_argument(
    '-w',
    dest='TwiceCompile',
    action='store_true',
    default=False,
    help='Compile twice.'
)
parser.add_argument(
    '-f',
    dest='FullCompile',
    action='store_true',
    default=False,
    help='Compile fully.'
)
parser.add_argument(
    '-l',
    dest='language',
    default='korean',
    help='Specify a language to sort index entries. For example, \"german\" or \"ger\" for German. The default is \"korean\".'
)
parser.add_argument(
    '-k',
    dest='KeepAux',
    action='store_true',
    default=False,
    help='Keep auxiliary files. This option is available only with full compilation (-f).'
)
parser.add_argument(
    '-m',
    dest='BookmarkIndex',
    action='store_true',
    default=False,
    help='Bookmark index entries which are Python functions extracted from docstrings.'
)
args = parser.parse_args()

# In case of a wrong filename extension
filename = os.path.splitext(args.tex[0])[0] 
tex = filename + '.tex'
idx = filename + '.idx'
ind = filename + '.ind'
if not os.path.exists(tex):
    msg = '%s is not found.' % (tex)
    print(msg)
    exit(False)

# Compile mode
if args.BatchMode or args.FullCompile:
    CompileMode = ' -interaction=batchmode '
else:
    CompileMode = ' -synctex=1 '
if args.ShellEscape:
    CompileMode += ' -shell-escape -8bit '

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

# Compile
cmd_tex = 'xelatex' + CompileMode + tex

def compile_fully():
    os.system(cmd_tex)
    os.system(cmd_tex)
    if os.path.exists(idx):
        cmd = 'texindy -M ' + ind_mod + idx
        os.system(cmd)        
        if args.BookmarkIndex:
            cmd = 'bmind.exe ' + ind
            os.system(cmd)
        os.system(cmd_tex)
    os.system(cmd_tex)
    if not args.KeepAux:
        os.system('texclean.exe')
            
if args.FullCompile:
    compile_fully()
elif args.TwiceCompile:
    os.system(cmd_tex)
    os.system(cmd_tex)
else:
    os.system(cmd_tex)
    