import os, glob, argparse, configparser, subprocess

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
parser = argparse.ArgumentParser(
    description='Change the resolution of image files using ImageMagick.'
)
parser.add_argument(
    'images',
    metavar='Image files',
    type=str,
    nargs='+',
    help='Specify PNG or JPG files to change their resolution.'
)
parser.add_argument(
    '-d',
    dest='density',
    type=int,
    default=80,
    help='Pixel density. Default: 80 (pixels per centimeter)'
)
parser.add_argument(
    '-m',
    dest='maxwidth',
    type=int,
    default=1000,
    help='Maximum width. Default: 1000 (pixels)'
)
parser.add_argument(
    '-s',
    dest='scale',
    type=int,
    default=100,
    help="Scale. Default: 100 (%%). If an image's width is 800 pixels and 50 is given for scale, the image is reduced to 400 pixels."
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
    exit(False)

# Resize the specified images.
widthlimit = args.maxwidth / args.density

def ResizeImage(image):
    cmd = '\"%s\" identify -ping -format %%w %s' %(args.magick, image)
    imgwidth = int(subprocess.check_output(cmd, stderr=subprocess.STDOUT))
    if imgwidth > args.maxwidth:
        density = imgwidth / widthlimit
    else:
        density = args.density
    cmd = '\"%s\" %s -units PixelsPerCentimeter -density %d -resize %d%% %s' % (args.magick, image, density, args.scale, image)
    os.system(cmd)

cnt = 0
for fnpattern in args.images:
    for image in glob.glob(fnpattern):        
        ResizeImage(image)        
        cnt += 1
msg = "%d image(s) have been resized." % (cnt)
print(msg)
