import os, glob, argparse, configparser, subprocess

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
parser = argparse.ArgumentParser(description='Change the resolution of image files using ImageMagick.')
parser.add_argument(
    'files',
    metavar='Image files',
    type=str,
    nargs='+',
    help='Specify PNG or JPG files to change their resolution.')
parser.add_argument(
    '-d',
    dest='density',
    type=int,
    nargs=1,
    default=80,
    help='Pixel density. Default: 80 (pixels per centimeter)')
parser.add_argument(
    '-m',
    dest='maxwidth',
    type=int,
    nargs=1,
    default=1000,
    help='Maximum width. Default: 100 (pixels)')
parser.add_argument(
    '-s',
    dest='scale',
    type=int,
    nargs=1,
    default=100,
    help="Scale. Default: 100 (%%). If an image's width is 800 pixels and 50 is given for scale, the image is reduced to 400 pixels.")
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

# Resize the specified images.
widthlimit = args.maxwidth / args.density

def ResizeImage(file):
    cmd = '\"%s\" identify -ping -format %%w %s' %(args.magick, file)
    imgwidth = int(subprocess.check_output(cmd, stderr=subprocess.STDOUT))
    if imgwidth > args.maxwidth:
        density = imgwidth / widthlimit
    else:
        density = args.density
    cmd = '\"%s\" %s -units PixelsPerCentimeter -density %d -resize %d%% %s' % (args.magick, file, density, args.scale, file)
    os.system(cmd)

cnt = 0
for pattern in args.files:
    for file in glob.glob(pattern):        
        ResizeImage(file)        
        cnt += 1
msg = "%d image(s) have been resized." % (cnt)
print(msg)
