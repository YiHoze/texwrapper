import os, sys, glob, argparse, configparser, subprocess

# Read the initiation file to get the path to a text editor and its option.
#ini = os.path.dirname(os.path.realpath(__file__)) + "\docenv.ini"
ini = os.path.split(sys.argv[0])[0] 
if bool(ini):
    ini += '\\docenv.ini'
else:
    ini = 'docenv.ini'
config = configparser.ConfigParser()
if os.path.exists(ini):
    config.read(ini)
    try:
        TextEditorPath = config.get('Text Editor', 'path')
    except:
        TextEditorPath = 'notepad.exe'
    try:
        TextEditorOption = config.get('Text Editor', 'option')
    except:
        TextEditorOption = ''
    try:
        associations = config.get('Text Editor', 'associations')
    except:
        associations = ['.txt', '.tex', '.sty', '.cls', '.idx', '.ind', '.log', '.bib']
else:
    TextEditorPath = 'notepad.exe'
    TextEditorOption = ''
    associations = ['.txt', '.tex', '.sty', '.cls', '.idx', '.ind', '.log', '.bib']

# Get arguments
parser = argparse.ArgumentParser(
    description='Open text files and others with an appropriate program.'
)
parser.add_argument(
    'files',
    type=str,
    nargs='+',
    help='Specify files to open.')
parser.add_argument(
    '-s',
    dest='texlive',
    action='store_true',
    default=False,
    help='Search TeX Live for the specified file to find and open.')
parser.add_argument(
    '-e',
    dest='editor',
    type=str,
    default=TextEditorPath,
    nargs=1,    
    help='Specify another text editor.')
parser.add_argument(
    '-o',
    dest='option',
    type=str,
    default=TextEditorOption,
    nargs=1,
    help='Specify an option for the text editor.')
args = parser.parse_args()

def DetermineFileType(file):
    ext = os.path.splitext(file)[1]        
    if ext.lower() in associations:
        return(True)
    else:
        return(False)

def OpenHere(files):
    for pattern in files:
        for file in glob.glob(pattern):
            if DetermineFileType(file):
                cmd = '\"%s\" %s %s' % (args.editor, args.option, file)                
                os.system(cmd)
            else:
                cmd = 'start %s' % (file)
                os.system(cmd)

def SearchTeXLive(files):
    for file in files:
        result = subprocess.check_output(['kpsewhich', file], stderr=subprocess.STDOUT)        
        gist = str(result, 'utf-8')
        if bool(gist):
            cmd = '\"%s\" %s %s' % (args.editor, args.option, gist)            
            os.system(cmd)
        else:
            msg = '%s is not found in TeX Live.' % (file)

if args.texlive:
    SearchTeXLive(args.files)
else:
    OpenHere(args.files)