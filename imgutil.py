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
    description = 'Change the resolution of image files using ImageMagick.'
)
parser.add_argument(
    'images',
    metavar = 'Image files',
    type = str,
    nargs = '+',
    help = 'Specify PNG or JPG files to change their resolution, or to view their image information.'
)
parser.add_argument(
    '-i',
    dest = 'image_info',
    action = 'store_true',
    default = False,
    help = 'Display image information.'
)
parser.add_argument(
    '-d',
    dest = 'density',
    type = int,
    default = 160,
    help = 'pixel density (default: 160 pixels per centimeter)'
)
parser.add_argument(
    '-m',
    dest = 'maxwidth',
    type = int,
    default = 1920,
    help = 'maximum width (default: 1920 pixels)'
)
parser.add_argument(
    '-s',
    dest = 'scale',
    type = int,
    default = 100,
    help = "scale (default: 100 %%) If an image's width is 800 pixels and 50 is given for scale, the image is reduced to 400 pixels."
)
parser.add_argument(
    '-p',
    dest = 'magick',  
    default = MagickPath, 
    help = 'Specify the path to another version of ImageMagick to use it.'
)
args = parser.parse_args()

# Check if ImageMagick is accessible.
try:
    cmd = args.magick + ' -version'
    subprocess.check_call(cmd)    
except OSError:
    print("Check the path to ImageMagick")
    exit(False)

# Resize the specified images.
widthlimit = args.maxwidth / args.density

def get_image_info(image):
    cmd = '\"%s\" identify -verbose %s' %(args.magick, image)
    result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    gist = str(result).split('\\r\\n')
    line = 4
    print('\n %s' %(image))
    while line < 8:
        print(gist[line])
        line += 1   

def resize_image(image):
    cmd = '\"%s\" identify -ping -format %%w %s' %(args.magick, image)
    imgwidth = int(subprocess.check_output(cmd, stderr = subprocess.STDOUT))
    if imgwidth > args.maxwidth:
        density = imgwidth / widthlimit
    else:
        density = args.density
    cmd = '\"%s\" -auto-orient -units PixelsPerCentimeter -density %d -resize %d%% %s %s' % (args.magick, density, args.scale, image, image)
    os.system(cmd)
    #print(cmd)

cnt = 0
for fnpattern in args.images:
    for image in glob.glob(fnpattern):
        if args.image_info:
            get_image_info(image)
        else:
            resize_image(image)        
            cnt += 1
if not args.image_info:
    msg = "%d image(s) have been resized." % (cnt)
    print(msg)
