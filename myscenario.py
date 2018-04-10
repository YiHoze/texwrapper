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

filename = os.path.splitext(args.output)[0]
tex = filename + '.tex'
pdf = filename + '.pdf'
if os.path.exists(tex):
    answer = input('%s already exists. Are you sure to overwrite it? [y/N] ' %(tex))
    if answer.lower() == 'y':
        os.remove(tex)
    else:
        sys.exit()

content = r"""\documentclass[10pt, openany]{hzguide}
\LayoutSetup{paper=A4, column=one}
\LayoutSetup{paper=A4, column=one}
\HeadingSetup{chapterstyle=tandh}
\setsecnumdepth{chapter}
\SectionNewpageOn
\DecolorHyperlinks
\CoverSetup{    
    FrontLogoImage = {alertsymbol},
    BackLogoImage = {alertsymbol},
    ProductImage = {uncertain},
    title = {Product X},
    DocumentType = {User Guide},
    PubYear = 2018,
    revision = {Rev. 1},
    note = {Keep this manual for later use.},
    manufacturer = Manufacturer,
    address = Seoul
}
\begin{document} 
\frontmatter* 
\FrontCover
\tableofcontents
\mainmatter*
\chapter{Introduction}\scenepara
\section{Features}\scenelist
\section{Package Items}\sceneimagetable
\section{Specifications}\scenespectables
\chapter{Safety}
\section{General Precautions}\scenelist[itemize][itemize]
\section{Tools}\sceneimagetable
\section{Safety Gear}\sceneimagetable
\chapter{Installation}
\section{Installation Requirements}\scenelist
\section{Installing X}\sceneprocedure[5]
\section{Checking X}\sceneprocedure
\section{Starting X}\scenelist*
\chapter{Operation}\scenetasks
\chapter{Troubleshooting}\listofproblems*\sceneproblems
\chapter{Maintenance}
\section{Precautions for Maintenance}\scenelist
\section{Scheduled Inspection}\scenelist
\chapter{Warranty}
\section{Warranty Coverage}\scenepara*
\section{Limitation of Liability}\scenepara*\scenelist
\section{Contact Information}\scenepara*
\appendix
\chapter{Technical Information}\scenespectables
\chapter{Glossary}\scenelist[terms]
\BackCover
\end{document}
"""

with open(tex, mode='w') as f:
    f.write(content)

os.system('powershell -command open.py %s' %(tex))

if not args.NoCompile:
    os.system('powershell -command xlt.py -b -w %s' %(tex))    
    os.system('powershell -command open.py %s' %(pdf))