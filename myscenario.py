import os, sys, argparse

parser = argparse.ArgumentParser(
    description = 'Generate a template for manuals.'
)

parser.add_argument(
    '-o',
    dest = 'output',
    default = 'manual',
    help = 'specify a filename (default: manual)'    
)
parser.add_argument(
    '-n',
    dest = 'NoCompile',
    action = 'store_true',
    default = False,
    help = 'pass over latex compilation'
)
args = parser.parse_args()

tex = args.output + '.tex'
pdf = args.output + '.pdf'
if os.path.exists(tex):
    answer = input('%s already exists. Are you sure to overwrite it? [y/N] ' %(tex))
    if answer.lower() == 'y':
        os.remove(tex)
    else:
        sys.exit()

content = """
\\documentclass[10pt,openany]{hzguide}
\\LayoutSetup{paper=A4, column=vartwo}
\\DecolorHyperlinks
\\title{Operation Manual}
\\date{}
\\begin{document} 
\\begin{IfVartwoEnlarge}
\\maketitle
\\end{IfVartwoEnlarge}
\\thispagestyle{empty}
\\newpage
\\SectionNewpageOn
\\tableofcontents*
\\chapter{Introduction}\\scenepara
\\section{Features}\\scenelist
\\section{Package Items}\\sceneimagetable
\\section{Specifications}\\scenespectables
\\chapter{Safety}
\\section{General Precautions}\\scenelist[itemize][itemize]
\\section{Tools}\\sceneimagetable
\\section{Safety Gear}\\sceneimagetable
\\chapter{Installation}
\\section{Installation Requirements}\\scenelist
\\section{Installing X}\\sceneprocedure[5]
\\section{Checking X}\\sceneprocedure
\\section{Starting X}\\scenelist*
\\chapter{Operation}\\scenetasks
\\chapter{Troubleshooting}\\listofproblems*\\sceneproblems
\\chapter{Maintenance}
\\section{Precautions for Maintenance}\\scenelist
\\section{Scheduled Inspection}\\scenelist
\\chapter{Warranty}
\\section{Warranty Coverage}\\scenepara*
\\section{Limitation of Liability}\\scenepara*\\scenelist
\\section{Contact Information}\\scenepara*
\\appendix
\\chapter{Technical Information}\\scenespectables
\\chapter{Glossary}\\scenelist[terms]
\\end{document}
"""

with open(tex, mode='w') as f:
    f.write(content)

if not args.NoCompile:
    os.system('xlt.exe -b -w %s' %(tex))
    os.system('open.exe %s' %(tex))
    os.system('open.exe %s' %(pdf))