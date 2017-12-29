import os, sys, argparse

parser = argparse.ArgumentParser(
    description = 'Create a tex file.'
)
parser.add_argument(
    '-f',
    dest = 'filename',
    default = 'mytex',
    help = 'specify a filename (default: mytex)'
)

parser.add_argument(
    '-c',
    dest = 'tex_class',
    default = 'hzguide',
    help = 'choose one among article, hzbeamer, hzguide, memoir, oblivoir'
)
args = parser.parse_args()

def tex_article():
    content = """\\documentclass{article}
\\usepackage{kotex}\n
\\begin{document}\n
\\end{document}"""
    return(content)

def tex_hzbeamer():
    content = """\\documentclass[10pt,flier=false,hangul=true]{hzbeamer}
\\usepackage{csquotes}
\\MakeOuterQuote{\"}
\\title{}
\\author{}
\\institute{}
\\date{}\n
\\begin{document}    
\\begin[fragile, allowframebreaks=1]{frame}{}\n
\\end{frame}
\\end{document}"""
    return(content)

def tex_hzguide():
    content = """\\documentclass[language=korean]{hzguide}
\\LayoutSetup{paper=A4}\n
\\begin{document}\n
\\end{document}"""
    return(content)

def tex_memoir():
    content = """\\documentclass[a4paper]{memoir} 
\\usepackage{fontspec}\n
\\begin{document}\n
\\end{document}"""
    return(content)

def tex_oblivoir():
    content = """\\documentclass[a4paper]{oblivoir} 
\\usepackage{fapapersize}
\\usefapapersize{*,*,30mm,*,30mm,*}\n
\\begin{document}\n
\\end{document}"""
    return(content)

tex = args.filename + '.tex'
if os.path.exists(tex):
    answer = input('%s already exists. Are you sure to overwrite it? [y/N] ' %(tex))
    if answer.lower() == 'y':
        os.remove(tex)
    else:
        sys.exit()

if args.tex_class == 'article':
    content = tex_article()
elif args.tex_class == 'hzbeamer':
    content = tex_hzbeamer()
elif args.tex_class == 'hzguide':
    content = tex_hzguide()
elif args.tex_class == 'memoir':
    content = tex_memoir()
elif args.tex_class == 'oblivoir':
    content = tex_hzbeamer()
else:
    content = tex_hzguide()

with open(tex, mode='w') as f:
    f.write(content)
os.system('open.exe %s' %(tex))
