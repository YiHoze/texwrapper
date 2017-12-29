import os, sys, argparse

try:
    dir_called = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    dir_called = False
if dir_called is False:
    dir_called = os.path.dirname(sys.argv[0])

examfile = os.path.join(dir_called, 'fontglyph.txt')

parser = argparse.ArgumentParser(
    description = 'Check what glyphs a font contains using an example text.'
)
parser.add_argument(
    'font',
    nargs = 1,
    help = "specify a font's filename"
)
parser.add_argument(
    '-e',
    dest = 'example',
    default = examfile,
    help = 'specify a file as an example text (default: fontglyph.txt)'
)
parser.add_argument(
    '-o',
    dest = 'output',  
    help = 'specify a name for output (default: font filename)'
)
args = parser.parse_args()

if not os.path.exists(args.example):
    print('%s is not found.' %(args.example))
    sys.exit()
else:
    with open(args.example, mode='r', encoding='utf-8') as f:
        text = f.readlines()
        text = ''.join(map(str, text))

if not bool(args.output):
    args.output = args.font

content = """
\\documentclass{minimal} 
\\usepackage{fontspec} 
\\setlength\\parskip{1.25\\baselineskip} 
\\setlength\\parindent{0pt}
\\setmainfont{%s}
\\begin{document}
%s
\\end{document}""" %(args.font[0], text)

filename = os.path.splitext(args.output)[0] 
tex = filename + '.tex'
pdf = filename + '.pdf'
if os.path.exists(tex):
    os.remove(tex)

with open(tex, mode='w', encoding='utf-8') as f:
    f.write(content)
os.system('xelatex %s' %(tex))
os.system('open.exe %s' %(pdf))
os.system('texclean.exe')