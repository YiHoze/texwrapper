import os, sys, glob, argparse, configparser

# Read the initiation file to get Jupyter templates.
try:
    inipath = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    inipath = False
if inipath is False:
    inipath = os.path.dirname(sys.argv[0])
ini = os.path.join(inipath, 'docenv.ini')
if os.path.exists(ini):
    config = configparser.ConfigParser()
    config.read(ini)
    try:
        latex_template = config.get('Jupyter Template', 'latex')
        latex_template = os.path.join(inipath, latex_template)
    except:
        print('Make sure to have docenv.ini set properly.')
        sys.exit()
else:
    print('Docenv.ini is not found. Set the DOCENV environment variable to the directory containing docenv.ini.')
    sys.exit()    

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
    help = 'To use another latex template, specify the path to it.'
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
            cmd = 'strrep.py ' + tex 
            os.system(cmd)
        # Compile latex
        if not args.passover:
            cmd = 'xelatex -interaction=batchmode %s' %(tex)
            os.system(cmd)
            os.system(cmd)
            os.system('texclean.py')
    else:
        print('%s is not a Jupyter notebook.' %(afile))

for fnpattern in args.ipynb:
    for afile in glob.glob(fnpattern):
        notebook_convert(afile)

