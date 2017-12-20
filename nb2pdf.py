import os, sys, glob, argparse, configparser

# Read the initiation file to get Jupyter templates.
ini = os.path.split(sys.argv[0])[0]
if bool(ini):
    inipath = ini
    ini += '\\docenv.ini'
else: # in case this source code is called by Python when the terminal's current directory is that which contains this script.
    inipath = '.'
    ini = 'docenv.ini'
config = configparser.ConfigParser()
if os.path.exists(ini):
    config.read(ini)
    try:
        latex_template = config.get('Jupyter Template', 'latex')
    except:
        latex_template = 'kari.tplx'
else:
    latex_template = 'kari.tplx'

if bool(inipath):    
    latex_template = inipath + '\\' + latex_template

parser = argparse.ArgumentParser(
    description = 'Convert Jupyter notebook files (.ipynb) to PDF using nbconvert and XeLaTeX.'
)
parser.add_argument(
    'ipynb',
    nargs = '+',
    help = 'Specify one or more Jupyter notebook files.'
)
parser.add_argument(
    '-t',
    dest = 'latex_template',
    default = latex_template,
    help = 'Path to your latex template (default: md2tex.tplx)'
)
parser.add_argument(
    '-e',
    dest = 'str_replacement',
    action = 'store_true',
    default = False,
    help = 'Replace some strings with others in the tex file.' 
)
parser.add_argument(
    '-p',
    dest = 'passover',
    action = 'store_true',
    default = False,
    help = 'Pass over the latex compilation process.'
)

args = parser.parse_args()

if not os.path.exists(args.latex_template):
    print('%s is not found.' %(args.latex_template))
    sys.exit()

def notebook_convert(afile):
    if afile.endswith('.ipynb'):    
        filename = os.path.splitext(afile)[0]
        tex = filename + '.tex'
        # Convert to latex
        cmd = 'jupyter nbconvert --to=latex --template=%s --SVG2PDFPreprocessor.enabled=True %s' %(args.latex_template, afile)
        os.system(cmd)
        # Replace strings
        if args.str_replacement:            
            cmd = 'strrep.exe ' + tex 
            os.system(cmd)
        # Compile latex
        if not args.passover:
            cmd = 'xelatex -interaction=batchmode %s' %(tex)
            os.system(cmd)
            os.system(cmd)
            os.system('texclean.exe')
    else:
        print('%s is not a Jupyter notebook.' %(afile))

for fnpattern in args.ipynb:
    for afile in glob.glob(fnpattern):
        notebook_convert(afile)

