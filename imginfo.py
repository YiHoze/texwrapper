import os, sys, glob, argparse, configparser, subprocess

# Read the initiation file to get the path to ImageMagick.
ini = os.path.split(sys.argv[0])[0] 
if bool(ini):
    ini += '\\docenv.ini'
else:
    ini = 'docenv.ini'
config = configparser.ConfigParser()
if os.path.exists(ini):
    config.read(ini)
    try:
        MagickPath = config.get('ImageMagick', 'path')
    except:
        MagickPath = r'C:\Program Files\ImageMagick-7.0.5-Q16\magick.exe'
else:
    MagickPath = r'C:\Program Files\ImageMagick-7.0.5-Q16\magick.exe'

# Get arguments
parser = argparse.ArgumentParser(description='View the metadata of image files using ImageMagick.')
parser.add_argument(
    'files',
    metavar='Image files',
    type=str,
    nargs='+',
    help='Specify PNG or JPG files to view their metadata.')
parser.add_argument(
    '-p',
    dest='magick',  
    default=MagickPath, 
    help='Path to ImageMagick')
args=parser.parse_args()

# Check if ImageMagick is accessible.
try:
    cmd = args.magick + ' -version'
    subprocess.check_call(cmd)    
except OSError:
    print("Check the path to ImageMagick")
    exit(False)

# Get
def GetImageInfo(file):
    cmd = '\"%s\" identify -verbose %s' % (args.magick, file)
    result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    gist = str(result).split('\\r\\n')
    line = 4
    while line < 8:
        print(gist[line])
        line += 1    

for pattern in args.files:
    for file in glob.glob(pattern):
        GetImageInfo(file)