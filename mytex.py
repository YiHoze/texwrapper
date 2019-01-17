import os, sys, glob, argparse

try:
    dir_called = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    dir_called = False
if dir_called is False:
    dir_called = os.path.dirname(sys.argv[0])

parser = argparse.ArgumentParser(
    description = 'Create a LaTeX file for one of the following purposes.'
)
parser.add_argument(
    'output',
    type = str,
    nargs = '?',
    help = 'Specify a filename for output.'
)
# parser.add_argument(
#     '-t',
#     dest = 'tex',
#     action = 'store_true',
#     default = False,
#     help = 'Create a latex file for free writing.' 
# )
parser.add_argument(
    '-cls',
    dest = 'tex_class',
    default = 'hzguide',
    help = 'Choose one among article, hzbeamer, hzguide, memoir, oblivoir. (default: hzguide)'
)
parser.add_argument(
    '-tpl',
    dest = 'template',
    action = 'store_true',
    default = False,
    help = 'Create an instruction manual template.' 
)
parser.add_argument(
    '-alb',
    dest = 'album',
    action = 'store_true',
    default = False,
    help = 'Create an album with image files in the current directory.'
)
parser.add_argument(
    '-s',
    dest = 'scale',
    default = '1',
    help = 'Image scale (default: 1)'
)
parser.add_argument(
    '-hid',
    dest = 'hide_image_name',
    action = 'store_true',
    default = False,
    help = 'Leave out filenames of images.'
)
parser.add_argument(
    '-k',
    dest = 'keep',
    action = 'store_true',
    default = False,
    help = 'Keep collateral files when creating an album.'
)
parser.add_argument(
    '-1',
    dest = 'one_column',
    action = 'store_true',
    default = False,
    help = 'Make the album\'s layout to be one column. (default: two columns)'
)
parser.add_argument(
    '-n',
    dest = 'no_compile',
    action = 'store_true',
    default = False,
    help = 'Pass over latex compilation.'
)
args = parser.parse_args()

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

def tex_article():
    content = """\\documentclass[a4paper]{article}
\\usepackage{fontspec}\n
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
\\begin{frame}[fragile, allowframebreaks=1]{}\n
\\end{frame}
\\end{document}"""
    return(content)

def tex_hzguide():
    content = """\\documentclass[language=korean]{hzguide}
\\LayoutSetup{}\n
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
    content = """\\documentclass{oblivoir} 
\\usepackage{fapapersize}
\\usefapapersize{*,*,30mm,*,30mm,*}\n
\\begin{document}\n
\\end{document}"""
    return(content)

def create_tex():
    if check_to_remove(tex) is False:
        return
    if args.tex_class == 'article':
        content = tex_article()
    elif args.tex_class == 'hzbeamer':
        content = tex_hzbeamer()
    elif args.tex_class == 'hzguide':
        content = tex_hzguide()
    elif args.tex_class == 'memoir':
        content = tex_memoir()
    elif args.tex_class == 'oblivoir':
        content = tex_oblivoir()
    else:
        content = tex_hzguide()
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)
    os.system('powershell -command open.py %s' %(tex))

def create_template():
    if check_to_remove(tex) is False:
        return    
    content = r"""\documentclass[10pt, openany]{hzguide}
\LayoutSetup{}
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
\chapter{Introduction}\tplpara
\section{Features}\tpllist
\section{Package Items}\tplimagetable
\section{Specifications}\tplspectables
\chapter{Safety}
\section{General Precautions}\tpllist[itemize][itemize]
\section{Tools}\tplimagetable
\section{Safety Gear}\tplimagetable
\chapter{Installation}
\section{Installation Requirements}\tpllist
\section{Installing X}\tplprocedure[5]
\section{Checking X}\tplprocedure
\section{Starting X}\tpllist*
\chapter{Operation}\tplactions
\chapter{Troubleshooting}\listofproblems*\tplproblems
\chapter{Maintenance}
\section{Precautions for Maintenance}\tpllist
\section{Scheduled Inspection}\tpllist
\chapter{Warranty}
\section{Warranty Coverage}\tplpara*
\section{Limitation of Liability}\tplpara*\tpllist
\section{Contact Information}\tplpara*
\appendix
\chapter{Technical Information}\tplspectables
\chapter{Glossary}\tpllist[terms]
\BackCover
\end{document}"""
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)
    os.system('powershell -command open.py %s' %(tex))
    if not args.no_compile:
        os.system('powershell -command ltx.py -b -w %s' %(tex))    
        os.system('powershell -command open.py %s' %(pdf))

def create_album():
    if check_to_remove(pdf) is False:
        return    
    # Make a file the contains a list of image files
    image_list = []
    image_type = ['pdf', 'jpg', 'jpeg', 'png']
    list_file = 't@mp.t@mp'
    for i in range(len(image_type)):
        fnpattern = '*.' + image_type[i]
        for afile in glob.glob(fnpattern):
            image_list.append(afile)
    image_list.sort()
    image_list = '\n'.join(map(str,image_list))
    with open(list_file, mode='w') as f:
        f.write(image_list)
    # Make a tex file with this content
    if args.one_column:
        content = """
        \\documentclass{hzguide}
        \\LayoutSetup{ulmargin=15mm, lrmargin=15mm}
        \\HeadingSetup{type=report}
        \\begin{document}
        \\MakeAlbum[%s]{%s}
        \\end{document}""" %(args.scale, list_file)
    else:
        content = """
        \\documentclass{hzguide}
        \\usepackage{multicol}
        \\LayoutSetup{ulmargin=15mm, lrmargin=15mm}
        \\HeadingSetup{type=report}
        \\begin{document}
        \\begin{multicols}{2}
        \\MakeAlbum[%s]{%s}
        \\end{multicols}
        \\end{document}""" %(args.scale, list_file)
    if args.hide_image_name:
        content = content.replace('MakeAlbum', 'MakeAlbum*')
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)
    os.system('powershell -command ltx.py -l -c %s' %(tex))
    os.system('powershell -command open.py %s' %(pdf))
    if not args.keep:
        os.remove(list_file)
        os.remove(tex)

if args.output is None:
    if args.template:
        output = 'manual'
    elif args.album:
        output = 'album'
    else:
        output = 'mytex'
else:
    output = args.output
tex = output + '.tex'
pdf = output + '.pdf'

if args.template:
    create_template()
elif args.album:
    create_album()
else:
    create_tex()
