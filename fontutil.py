import os, sys, argparse

try:
    dir_called = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    dir_called = False
if dir_called is False:
    dir_called = os.path.dirname(sys.argv[0])

examfile = os.path.join(dir_called, 'fontglyph.txt')

parser = argparse.ArgumentParser(
    description = 'View the list of installed fonts, or see what glyphs a font contains using XeLaTeX and example text.'
)
parser.add_argument(
    'font',
    nargs = '?',
    help = "a font's filename (foo.ttf)"
)
parser.add_argument(
    '-l',
    dest = 'font_list',
    default = 'font_list.txt',
    help = 'a filename for list of fonts (default: font_list.txt)'
)
parser.add_argument(
    '-e',
    dest = 'example',
    default = examfile,
    help = 'a file as example text (default: fontglyph.txt)'
)
parser.add_argument(
    '-o',
    dest = 'output',  
    help = 'a filename for output of glyphs (default: font filename)'
)
args = parser.parse_args()

def show_glyphs():
    if not os.path.exists(args.example):
        print('%s is not found.' %(args.example))
        sys.exit()
    else:
        with open(args.example, mode='r', encoding='utf-8') as f:
            text = f.readlines()
            text = ''.join(map(str, text))
    if args.output is None:
        args.output = args.font
    filename = os.path.splitext(args.output)[0] 
    tex = filename + '.tex'
    pdf = filename + '.pdf'
    if os.path.exists(tex):
        answer = input('%s already exists. Are you sure to remake it? [y/N] ' %(tex))
        if answer.lower() == 'y':
            os.remove(tex)
        else:
            sys.exit()
    content = """
    \\documentclass{minimal} 
    \\usepackage{fontspec} 
    \\setlength\\parskip{1.25\\baselineskip} 
    \\setlength\\parindent{0pt}
    \\setmainfont{%s}
    \\begin{document}
    %s
    \\end{document}""" %(args.font, text)
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)
    os.system('powershell -command ltx.py -c %s' %(tex))
    os.system('powershell -command open.py %s' %(pdf))

def enumerate_fonts():
    if os.path.exists(args.font_list):
        os.remove(args.font_list)
    cmd = "fc-list : file >> %s" %(args.font_list)
    os.system(cmd)
    with open(args.font_list, mode='r', encoding='utf-8') as f:
        content = f.readlines()
    content.sort()
    #content = ''.join(map(str, content))
    with open(args.font_list, mode='w', encoding='utf-8') as f:
        for line in content:
            f.write(os.path.basename(line))
            # f.write(line)
    os.system("powershell -command open.py %s" %(args.font_list))

if args.font is None:
    enumerate_fonts()
else:
    show_glyphs()