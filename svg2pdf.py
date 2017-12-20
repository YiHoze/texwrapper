import os, sys, glob, argparse, configparser, subprocess

# Read the initiation file to get the path to Inkscape.
ini = os.path.split(sys.argv[0])[0] 
if bool(ini):
    ini += '\\docenv.ini'
else: # in case this source code is called by Python when the terminal's current directory is that which contains this script.
    ini = 'docenv.ini'
config = configparser.ConfigParser()
if os.path.exists(ini):
    config.read(ini)
    try:
        InkscapePath = config.get('Inkscape', 'path')
    except:
        InkscapePath = r'C:\Program Files\Inkscape\inkscape.com'
else:
    InkscapePath = r'C:\Program Files\Inkscape\inkscape.com'

# Get arguments
parser = argparse.ArgumentParser(description='Convert SVG to PDF using Inkscape.')
parser.add_argument(
    'files', 
    metavar='SVG', 
    type=str, 
    nargs='*', 
    help='If no SVG file is specified, every SVG file in the current directory is to be converted.')
parser.add_argument(
    '-p',
    dest='inkscape',  
    default=InkscapePath, 
    help='Path to Inkscape')
parser.add_argument(
    '-n',
    dest='crop',    
    action='store_false',
    default=True,
    help='Do not remove white margins (default: crop)')
args = parser.parse_args()

# Check if Inkscape and PDFCROP are accessible.
try:
    cmd = args.inkscape + ' --version'
    subprocess.check_call(cmd)
except OSError:
    print("Check the path to Inkscape.")
    exit(False)
try:
    subprocess.check_call('pdfcrop.exe --version')
except OSError:
    print("Make sure TeX Live is included in PATH.")
    exit(False)

# Convert the specified SVG files to PDF.
def svg2pdf(afile):
    if afile.endswith('.svg'):        
        target = os.path.splitext(afile)[0] + '.pdf'
        cmd = "\"%s\" --export-pdf %s %s" % (args.inkscape, target, afile)
        os.system(cmd)        
        if args.crop:
            cmd = "pdfcrop.exe %s %s" % (target, target)
            os.system(cmd)
    else:
        print('%s is not SVG' %(afile))

cnt = 0
if not bool(args.files):
    for afile in glob.glob('*.svg'):
        svg2pdf(afile)
        cnt += 1        
else:
    for fnpattern in args.files:
        for afile in glob.glob(fnpattern):
            svg2pdf(afile)
            cnt += 1
msg = "%d file(s) have been converted." % (cnt)
print(msg)