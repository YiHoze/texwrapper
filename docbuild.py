import os, glob, argparse

# Get arugments.
parser = argparse.ArgumentParser(
    description = 'This is a wrapper program to automate the build process using Sphinx and XeLaTeX.'
)
parser.add_argument(
    'target',
    nargs = '*',
    help = 'Choose either html or latex.'
)
parser.add_argument(
    '-s',
    dest = 'SourceDir',
    default = '.',
    help = 'Source directory (default: .)'    
)
parser.add_argument(
    '-b',
    dest = 'BuildDir',    
    default = '_build',
    help = 'Build directory (default: _build)'
)
parser.add_argument(
    '-t',
    dest = 'tex',
    help = 'TeX filename'
)
parser.add_argument(
    '-o',
    dest = 'OnceCompile',
    action = 'store_true',
    default = False,
    help = 'Compile once.'
)
parser.add_argument(
    '-w',
    dest = 'TwiceCompile',
    action = 'store_true',
    default = False,
    help = 'Compile twice.'
)
parser.add_argument(
    '-f',
    dest = 'FullCompile',
    action = 'store_true',
    default = False,
    help = 'Compile fully.'
)
parser.add_argument(
    '-l',
    dest = 'language',
    default = 'korean',
    help = 'Specify a language to sort index entries. For example, \'german\' or \'ger\' for German. The default is \'korean\'.'
)
parser.add_argument(
    '-j',
    dest = 'AutoJosa',
    action = 'store_true',
    default = False,
    help = 'Replace with 자동조사.'
)
parser.add_argument(
    '-e',
    dest = 'str_replacement',
    action = 'store_true',
    default = False,
    help = 'Replace some strings with others in the tex file.'
)
parser.add_argument(
    '-k',
    dest = 'KeepAux',
    action = 'store_true',
    default = False,
    help = 'Keep auxiliary files. This option is available only with full compilation (-f).'
)
parser.add_argument(
    '-m',
    dest = 'BookmarkIndex',
    action = 'store_true',
    default = False,
    help = 'Bookmark index entries which are Python functions extracted from docstrings.'
)
parser.add_argument(
    '-c',
    dest = 'clean',
    action = 'store_true',
    default = False,
    help = 'Clean the build directory.'
)
parser.add_argument(
    '-r',
    dest = 'refresh',
    action = 'store_true',
    default = False,
    help = 'Read and write all files anew.'
)
parser.add_argument(
    '-p',
    dest = 'passover',
    action = 'store_true',
    default = False,
    help = 'Pass over the image processing.'
)
args = parser.parse_args()

def build_html():
    cmd = 'sphinx-build -M html %s %s' % (args.SourceDir, args.BuildDir)
    if args.refresh:
        cmd +=  ' -e -E'
    os.system(cmd)

def build_latex():        
    files = LatexDir + '/blockdiag-*.pdf'
    for afile in glob.glob(files):    
        os.remove(afile)
    cmd = 'sphinx-build -M latex %s %s' % (args.SourceDir, args.BuildDir)
    if args.refresh:
        cmd +=  ' -e -E'
    os.system(cmd)
    os.chdir(LatexDir)    
    if not args.passover:
        if os.path.exists('images'):
            cmd = 'svg2pdf.exe images/*.svg'
            os.system(cmd)
        for afile in glob.glob('blockdiag-*.pdf'):
            cmd = 'pdfcrop.exe %s %s' %(afile, afile)
            os.system(cmd)
    if args.str_replacement:
        cmd = 'strrep.exe ' + tex 
        os.system(cmd)
    if args.AutoJosa:
        cmd = 'autojosa.exe ' + tex
        os.system(cmd)
    if args.FullCompile:
        compile_fully()
    elif args.TwiceCompile:
        os.system(cmd_tex)
        os.system(cmd_tex)
    elif args.OnceCompile:
        os.system(cmd_tex)
    os.chdir('../..')

def clean_build():
    cmd = 'sphinx-build -M clean %s %s' % (args.SourceDir, args.BuildDir)
    os.system(cmd)

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
        files = ['sphinxhowto.cls', 'sphinxmanual.cls', 'sphinx.sty', 'python.ist', 'Makefile', 'latexmkrc', 'latexmkjarc']
        for afile in files:
            os.remove(afile)

# In case of a wrong filename extension
LatexDir = args.BuildDir + '/latex'
filename = os.path.splitext(args.tex)[0] 
tex = filename + '.tex'
idx = filename + '.idx'
ind = filename + '.ind'
# Latex compile mode
if args.FullCompile:
    CompileMode = ' -interaction=batchmode '
else:
    CompileMode = ' -synctex=1 '
cmd_tex = 'xelatex %s %s' %(CompileMode, tex)
# Choose a language to sort the index
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

if args.clean:
    clean_build()      
elif args.target[0] == 'html':
    build_html()
elif args.target[0] == 'latex':
    build_latex()
    
    