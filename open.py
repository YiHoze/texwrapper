import os, sys, glob, argparse, configparser, subprocess

# Read the initiation file to get the path to a text editor and its option.
try:
    inipath = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    inipath = False
if inipath is False:
    inipath = os.path.dirname(sys.argv[0]) # the directory where this script exists.
ini = os.path.join(inipath, 'docenv.ini')
if os.path.exists(ini):
    config = configparser.ConfigParser()
    config.read(ini)
    try:
        TextEditorPath = config.get('Text Editor', 'path')
        TextEditorOption = config.get('Text Editor', 'option')
        associations = config.get('Text Editor', 'associations')
    except:
        print('Make sure to have docenv.ini set properly.')
        sys.exit()
else:
    print('Docenv.ini is not found. Set the DOCENV environment variable to the directory containing docenv.ini.')
    sys.exit() 

# Get arguments
parser = argparse.ArgumentParser(
    description='Open text files and others with an appropriate program.'
)
parser.add_argument(
    'files',
    type=str,
    nargs='+',
    help='Specify files to open.'
)
parser.add_argument(
    '-s',
    dest='texlive',
    action='store_true',
    default=False,
    help='Search TeX Live for the specified file to find and open.'
)
parser.add_argument(
    '-e',
    dest='editor',
    type=str,
    default=TextEditorPath,
    nargs=1,    
    help='Specify another text editor to use it.'
)
parser.add_argument(
    '-o',
    dest='option',
    type=str,
    default=TextEditorOption,
    nargs=1,
    help='Specify another editor option to use it.'
)
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