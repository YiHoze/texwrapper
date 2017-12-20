import os, sys, glob, argparse, configparser, subprocess

# Read the initiation file to get the path to a text editor and its option.
#ini = os.path.dirname(os.path.realpath(__file__)) + "\docenv.ini"
ini = os.path.split(sys.argv[0])[0] 
if bool(ini):
    ini += '\\docenv.ini'
else: # in case this source code is called by Python when the terminal's current directory is that which contains this script.
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

def DetermineFileType(afile):
    ext = os.path.splitext(afile)[1]        
    if ext.lower() in associations:
        return(True)
    else:
        return(False)

def OpenHere(files):
    for fnpattern in files:
        for afile in glob.glob(fnpattern):
            if DetermineFileType(afile):
                cmd = '\"%s\" %s %s' % (args.editor, args.option, afile)
                os.system(cmd)
            else:
                cmd = 'start %s' % (afile)
                os.system(cmd)

def SearchTeXLive(files):
    for afile in files:        
        try:
            result = subprocess.check_output(['kpsewhich', afile], stderr=subprocess.STDOUT)
            gist = str(result, 'utf-8')
            cmd = '\"%s\" %s %s' % (args.editor, args.option, gist)            
            os.system(cmd)
        except subprocess.CalledProcessError:
                print('%s is not found in TeX Live.' % (afile))

if args.texlive:
    SearchTeXLive(args.files)
else:
    OpenHere(args.files)