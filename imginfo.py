import os, sys, glob, argparse, configparser, subprocess

# Read the initiation file to get the path to ImageMagick.
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
        MagickPath = config.get('ImageMagick', 'path')
    except:
        print('Make sure to have docenv.ini set properly.')
        sys.exit()
else:
    print('Docenv.ini is not found. Set the DOCENV environment variable to the directory containing docenv.ini.')
    sys.exit()    

# Get arguments
parser = argparse.ArgumentParser(description='View the basic information of image files using ImageMagick.')
parser.add_argument(
    'images',
    metavar='Image files',
    type=str,
    nargs='+',
    help='Specify PNG or JPG files to view their basic information.'
)
parser.add_argument(
    '-p',
    dest='magick',  
    default=MagickPath, 
    help='To use another version of ImageMagick, specify the path to it.'
)
args=parser.parse_args()

# Check if ImageMagick is accessible.
try:
    cmd = args.magick + ' -version'
    subprocess.check_call(cmd)    
except OSError:
    print("Check the path to ImageMagick")
    sys.exit()

# Get
def GetImageInfo(afile):
    cmd = '\"%s\" identify -verbose %s' % (args.magick, afile)
    result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    gist = str(result).split('\\r\\n')
    line = 4
    print('\n %s' %(afile))
    while line < 8:
        print(gist[line])
        line += 1    

for fnpattern in args.images:
    for afile in glob.glob(fnpattern):
        GetImageInfo(afile)