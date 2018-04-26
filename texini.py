import os, sys, glob, argparse, configparser
import subprocess

# Read the initiation file to get the data required for configuration of the environment for latex.
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
else:
    print('Docenv.ini is not found. Set the DOCENV environment variable to the directory containing docenv.ini.')
    sys.exit()

# Get arguments
parser = argparse.ArgumentParser(
    description ='Configure your environment for LaTeX.'
)
parser.add_argument(
    '-c',
    dest = 'copy_to_local',
    action = 'store_true',
    default = False,
    help = 'Copy the provided latex style files into the local TeXMF directory.'
)
parser.add_argument(
    '-d',
    dest = 'docenv',
    action = 'store_true',
    default = False,
    help = 'Specify the directory where executable files and relevant files of this documentation system are located to set the path as an environment variable.'
)
parser.add_argument(
    '-p',
    dest = 'sumatrapdf',
    action = 'store_true',
    default = False,
    help = 'Set SumatraPDF to enable inverse search. (jumping back to the corresponding point in the source tex file)'
)
parser.add_argument(
    '-e',
    dest = 'texedit',
    action = 'store_true',
    default = False,
    help = 'Set TEXEDIT as an environment variable.'
)
parser.add_argument(
    '-t',
    dest = 'texmfhome',
    action = 'store_true',
    default = False,
    help = 'Set TEXMFHOME as an environment variable.'
)
parser.add_argument(
    '-f',
    dest = 'cache_font',
    action = 'store_true',
    default = False,
    help = 'Cache fonts for xelatex.'
)
parser.add_argument(
    '-u',
    dest = 'update_texlive',
    action = 'store_true',
    default = False,
    help = 'Update TeX Live.'
)
args = parser.parse_args()

def copy_to_local():
    print('\n[Copying latex style files]')
    if not (config.has_option('Sphinx Style', 'latex') and 
        config.has_option('TeX Live', 'texmflocal')):
        print('Make sure to have docenv.ini set properly.')
        sys.exit()
    else:
        latex_style = config.get('Sphinx Style', 'latex')
        texmf_local = config.get('TeX Live', 'texmflocal')
    answer = input('These files are going to be copied into <%s>\n%s\nEnter Y to proceed, N to abandon, or another directory: ' %(texmf_local, latex_style.replace(', ', '\n')))
    if (answer.lower() == 'n'):
        return
    if not (answer.lower() == 'y' or answer == ''):
        texmf_local = answer
    files = latex_style.split()
    for afile in files:        
        src = os.path.join(inipath, afile)
        cmd = 'copy %s %s' %(src, texmf_local) 
        os.system(cmd)        
    dst = os.path.join(texmf_local, '*.*')
    for afile in glob.glob(dst):
        print(afile)
    os.system('mktexlsr')

def set_docenv():
    print('\n[Setting DOCENV]')
    if not config.has_option('DocEnv', 'path'):
        print('Make sure to have docenv.ini set properly.')
        return
    docenv = config.get('DocEnv', 'path')
    answer = input('Are you sure to set the DOCENV environment variable to <%s>?\nEnter [Y] to proceed, [n] to abandon, or another directory: ' %(docenv))
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        docenv = answer
    cmd = "powershell \"set-itemproperty -path HKCU:\Environment -name DOCENV -value '%s'\"" % (docenv)
    os.system(cmd)
    cmd = "powershell \"(get-itemproperty -path HKCU:\Environment).'DOCENV'\""
    os.system(cmd)

def set_texedit():
    print('\n[Setting TEXEDIT]')
    if not config.has_option('TeX Live', 'TEXEDIT'):
        print('Make sure to have docenv.ini set properly.')
        return
    texedit = config.get('TeX Live', 'TEXEDIT')
    answer = input('Are you sure to set the TEXEDIT environment variable to  <%s>?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: ' %(texedit))
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        texedit = answer
    cmd = "powershell \"set-itemproperty -path HKCU:\Environment -name TEXEDIT -value '%s'\"" % (texedit)
    os.system(cmd)
    cmd = "powershell \"(get-itemproperty -path HKCU:\Environment).'TEXEDIT'\""
    os.system(cmd)

def set_texmfhome():
    print('\n[Setting TEXMFHOME]')
    if not config.has_option('TeX Live', 'TEXMFHOME'):
        print('Make sure to have docenv.ini set properly.')
        return
    texedit = config.get('TeX Live', 'TEXMFHOME')
    answer = input('Are you sure to set the TEXMFHOME environment variable to  <%s>?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: ' %(texedit))
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        texedit = answer
    cmd = "powershell \"set-itemproperty -path HKCU:\Environment -name TEXMFHOME -value '%s'\"" % (texedit)
    os.system(cmd)
    cmd = "powershell \"(get-itemproperty -path HKCU:\Environment).'TEXMFHOME'\""
    os.system(cmd)

def update_texlive():
    print('\n[Updating TeX Live]')
    if not config.has_option('TeX Live', 'repository'):
        print('Make sure to have docenv.ini set properly.')
        return
    repository = config.get('TeX Live', 'repository')
    answer = input('Are you sure to use the <%s> repository to update the TeX Live?\nEnter [Y] to proceed, [n] to abandon, or another repository: ' %(repository))
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        repository = answer
    cmd = 'tlmgr option repository %s' %(repository)
    os.system(cmd)
    cmd = 'tlmgr update --self --all'
    os.system(cmd)

def set_sumatrapdf():
    print('\n[Setting SumatraPDF')
    if not (config.has_option('SumatraPDF', 'path') and config.has_option('SumatraPDF', 'inverse-search')):
        print('Make sure to have docenv.ini set properly.')
        return
    sumatra = config.get('SumatraPDF', 'path')
    editor = config.get('SumatraPDF', 'inverse-search')
    answer = input('Are you sure to use <%s> to enable the inverse search feature of SumatraPDF?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: ' %(editor))
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        editor = answer    
    cmd = []
    cmd.append(sumatra)
    cmd.append('-inverse-search')
    cmd.append(editor)    
    subprocess.Popen(cmd)

def cache_font():
    print('\n[Caching fonts]')
    answer = input('Are you sure to cache fonts?\nEnter [Y] to proceed or [n] to abandon: ')
    if (answer.lower() == 'y' or answer == ''):
        cmd = 'fc-cache -v -r'
        os.system(cmd)        

if args.copy_to_local:
    copy_to_local()
if args.docenv:
    set_docenv()
if args.update_texlive:
    update_texlive()
if args.texedit:
    set_texedit()
if args.texmfhome:
    set_texmfhome()
if args.sumatrapdf:
    set_sumatrapdf()
if args.cache_font:
    cache_font()
