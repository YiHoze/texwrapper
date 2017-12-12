import os, sys, glob, argparse, configparser

# Read the initiation file to get Jupyter templates.
ini = os.path.split(sys.argv[0])[0]
if bool(ini):
    inipath = ini
    ini += '\\docenv.ini'
else:
    ini = 'docenv.ini'
config = configparser.ConfigParser()
if os.path.exists(ini):
    config.read(ini)
    try:
        markdown_template = config.get('Jupyter Template', 'markdown')
    except:
        markdown_template = 'nb2md.tpl'
    try:
        latex_template = config.get('Jupyter Template', 'latex')
    except:
        latex_template = 'md2tex.tplx'
else:
    markdown_template = 'nb2md.tpl'
    latex_template = 'md2tex.tplx'

if bool(inipath):
    markdown_template = inipath + '\\' + markdown_template 
    latex_template = inipath + '\\' + latex_template

parser = argparse.ArgumentParser(
    description = 'nb2pdf.exe takes three steps to create a PDF from a single Jupyter notebook as follows: \
        1) lets nbconvert convert the specified .ipynb file to markdown (.md);  \
        2) lets pandoc convert the markdown file to latex (.tex);  \
        3) finally lets xelatex create a PDF from the latex file.'
)
parser.add_argument(
    'ipynb',
    nargs = '+',
    help = 'Specify one or more Jupyter notebook files.'
)
parser.add_argument(
    '-m',
    dest = 'markdown_template',
    default = markdown_template,
    help = 'Path to your markdown template (default: nb2md.tpl)'
)
parser.add_argument(
    '-t',
    dest = 'latex_template',
    default = latex_template,
    help = 'Path to your latex template (default: md2tex.tplx)'
)
args = parser.parse_args()

if not os.path.exists(args.markdown_template):
    print('%s is not found.' %(args.markdown_template))
    sys.exit()
if not os.path.exists(args.latex_template):
    print('%s is not found.' %(args.latex_template))
    sys.exit()

def notebook_convert(file):
    if file.endswith('.ipynb'):    
        filename = os.path.splitext(file)[0]
        md = filename + '.md'
        tex = filename + '.tex'
        # Convert to markdown
        cmd = 'jupyter nbconvert --to=markdown --template=%s --SVG2PDFPreprocessor.enabled=True %s' %(args.markdown_template, file)
        os.system(cmd)
        # Convert to latex
        cmd = 'pandoc -f markdown -t latex -o %s --template=%s %s' %(tex, args.latex_template, md)
        os.system(cmd)
        # Compile latex
        cmd = 'xelatex -interaction=batchmode %s' %(tex)
        os.system(cmd)
        os.system(cmd)
        os.system('texclean.exe')
    else:
        print('%s is not a Jupyter notebook.' %(file))

for file_pattern in args.ipynb:
    for file in glob.glob(file_pattern):
        notebook_convert(file)

