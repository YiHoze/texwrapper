import os, sys, glob, argparse, configparser, subprocess

# Read the initiation file to get the path to Inkscape.
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
        InkscapePath = config.get('Inkscape', 'path')
    except:
        print('Make sure to have docenv.ini set properly with Inkscape.')
        InkscapePath = 'inkscape.com'
    try:
        MagickPath = config.get('ImageMagick', 'path')
    except:
        print('Make sure to have docenv.ini set properly with ImageMagick.')  
        MagickPath = 'magick.exe'
else:
    print('Docenv.ini is not found. Set the DOCENV environment variable to the directory containing docenv.ini.' )

# Get arguments
parser = argparse.ArgumentParser(
    description = 'This script requires TeX Live, Inkscape, and ImageMagick. With this script you can: 1) view a bitmap image\'s information; 2) resize a bitmap image by changing its resolution or scale; 3) convert a bitmap image to another format [jpg/png]; 4) convert a vector image to another vector or bitmap format [eps/pdf/svg to pdf/eps/jpg/png]. Be aware that SVG cannot be the target format.'
)
parser.add_argument(
    'image',
    nargs = '+',
    help = 'Specify one or more images.'
)
parser.add_argument(
    '-i',
    dest = 'view_info',
    action = 'store_true',
    default = False,
    help = 'Display image information.'
)
parser.add_argument(
    '-t',
    dest = 'target_format',
    default = 'pdf',
    help = 'Specify the target format. (default: pdf)'
)
parser.add_argument(
    '-r',
    dest = 'resize',
    action = 'store_true',
    default = False,
    help = 'Change resolution or scale.'
)
parser.add_argument(
    '-d',
    dest = 'density',
    type = int,
    # default = 100,
    help = 'Pixel density (default: 100 pixels per centimeter for bitmap and 254 for vector)'
)
parser.add_argument(
    '-m',
    dest = 'maxwidth',
    type = int,
    default = 1920,
    help = 'Maximum width (default: 1920 pixels)'
)
parser.add_argument(
    '-s',
    dest = 'scale',
    type = int,
    default = 100,
    help = "Scale (default: 100 %%). If an image's width is 800 pixels and 50 is given for scale, the image is reduced to 400 pixels."
)
parser.add_argument(
    '-g',
    dest = 'gray',
    action = 'store_true',
    default = False,
    help = 'Covert to grayscale.'
)
parser.add_argument(
    '-rec',
    dest = 'recursive',
    action = 'store_true',
    default = False,
    help = 'process ones in all subdirectories'
)

args = parser.parse_args()
cnt = 0

def check_TeXLive_exists():
    try:
        subprocess.check_call('epstopdf.exe --version')
    except OSError:
        print("Make sure TeX Live is included in PATH.")
        sys.exit()

def check_Inkscape_exists():
    try:
        cmd = InkscapePath + ' --version'
        subprocess.check_call(cmd)
    except OSError:
        print("Check the path to Inkscape.")
        sys.exit()

def check_ImageMagick_exists():
    try:
        cmd = MagickPath + ' --version'
        subprocess.check_call(cmd)
    except OSError:
        print("Check the path to ImageMagick.")
        sys.exit()

def check_converter(fnpattern):    
    srcfmt = os.path.splitext(fnpattern)[1]
    srcfmt = srcfmt.lower()
    if args.view_info:
        check_ImageMagick_exists()
    if args.resize:
        check_ImageMagick_exists()
    elif trgfmt == '.png' or trgfmt == '.jpg':
        check_ImageMagick_exists()
    elif srcfmt == '.svg':
        check_Inkscape_exists()
    else:
        check_TeXLive_exists()

def eps_to_pdf(src):
    global cnt
    os.system('epstopdf.exe %s' %(src))
    cnt += 1

def pdf_to_eps(src):
    global cnt 
    os.system('pdftops -eps %s' %(src))
    cnt += 1

def svg_to_pdf(src, trg):
    global cnt
    cmd = "\"%s\" --export-pdf %s %s" % (InkscapePath, trg, src)
    os.system(cmd)
    cnt += 1
    cmd = "pdfcrop.exe %s %s" % (trg, trg)
    os.system(cmd)

def svg_to_eps(src, trg):
    global cnt
    cmd = "\"%s\" --export-eps %s %s" % (InkscapePath, trg, src)
    cnt += 1
    os.system(cmd)

def bitmap_to_bitmap(src, trg):
    global cnt
    if args.gray:
        cmd = '\"%s\" %s -colorspace gray %s' %(MagickPath, src, trg)
    else:
        cmd = '\"%s\" %s %s' %(MagickPath, src, trg)
    os.system(cmd)
    cnt += 1

def vector_to_bitmap(src, trg):
    global cnt
    if args.density is None:
        density = 254
    else: 
        density = args.density
    cmd = '\"%s\" -density %d %s %s' %(MagickPath, density, src, trg)
    os.system(cmd)
    multiple = density / 100
    density = int(density / multiple)
    cmd = '\"%s\" %s -units PixelsPerCentimeter -density %d %s' % (MagickPath, trg, density, trg)
    os.system(cmd)    
    cnt += 1

def get_bitmap_info(img):
    cmd = '\"%s\" identify -verbose %s' %(MagickPath, img)
    result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    gist = str(result).split('\\r\\n')
    line = 4
    print('\n %s' %(img))
    while line < 8:
        print(gist[line])
        line += 1   

def resize_bitmap(img):
    global cnt
    if args.density is None:
        density = 100
    else: 
        density = args.density
    widthlimit = args.maxwidth / density
    cmd = '\"%s\" identify -ping -format %%w %s' %(MagickPath, img)
    imgwidth = int(subprocess.check_output(cmd, stderr = subprocess.STDOUT))
    if imgwidth > args.maxwidth:
        density = imgwidth / widthlimit    
    cmd = '\"%s\" %s -auto-orient -units PixelsPerCentimeter -density %d -resize %d%%  %s' % (MagickPath, img, density, args.scale, img)
    os.system(cmd)    
    cnt += 1

def get_subdirs(fnpattern):
    curdir = os.path.dirname(fnpattern)
    if curdir == '':
        curdir = '.'
    return([x[0] for x in os.walk(curdir)])

def converter(afile):
    basename, srcfmt = os.path.splitext(afile)
    srcfmt = srcfmt.lower()
    target = basename + trgfmt
    if srcfmt == '.eps':
        if trgfmt == '.pdf':
            eps_to_pdf(afile)
        elif trgfmt == '.jpg':
            vector_to_bitmap(afile, target)
        elif trgfmt == '.png':
            vector_to_bitmap(afile, target)
    elif srcfmt == '.pdf':
        if trgfmt == '.eps':
            pdf_to_eps(afile)
        elif trgfmt == '.jpg':
            vector_to_bitmap(afile, target)
        elif trgfmt == '.png':
            vector_to_bitmap(afile, target)
    elif srcfmt == '.svg':
        if trgfmt == '.pdf':
            svg_to_pdf(afile, target)
        elif trgfmt == '.eps':
            svg_to_eps(afile, target)
        elif trgfmt == '.jpg':
            vector_to_bitmap(afile, target)
        elif trgfmt == '.png':
            vector_to_bitmap(afile, target)
    elif srcfmt == '.png':
        if trgfmt == '.jpg':
            bitmap_to_bitmap(afile, target)
        elif trgfmt == '.pdf':
            bitmap_to_bitmap(afile, target)
    elif srcfmt == '.jpg':
        if trgfmt == '.png':
            bitmap_to_bitmap(afile, target)
        elif trgfmt == '.pdf':
            bitmap_to_bitmap(afile, target)
    elif srcfmt == '.ppm':
        if trgfmt == '.jpg':
            bitmap_to_bitmap(afile, target)
        elif trgfmt == '.png':
            bitmap_to_bitmap(afile, target)
    elif srcfmt == '.pbm':
        if trgfmt == '.jpg':
            bitmap_to_bitmap(afile, target)
        elif trgfmt == '.png':
            bitmap_to_bitmap(afile, target)
    elif srcfmt == '.webp':
        if trgfmt == '.jpg':
            bitmap_to_bitmap(afile, target)
        elif trgfmt == '.png':
            bitmap_to_bitmap(afile, target)
    elif srcfmt == '.cr2':
        if trgfmt == '.jpg':
            bitmap_to_bitmap(afile, target)
        elif trgfmt == '.png':
            bitmap_to_bitmap(afile, target)

trgfmt = args.target_format
trgfmt = trgfmt.lower()
if not trgfmt.startswith('.'):
    trgfmt = '.' + trgfmt

for fnpattern in args.image: 
    check_converter(fnpattern)   
    if args.recursive:
        filename = os.path.basename(fnpattern)        
        subdirs = get_subdirs(fnpattern)
        for subdir in subdirs:
            subfile = os.path.join(subdir, filename)
            for afile in glob.glob(subfile):
                if args.view_info:
                    get_bitmap_info(afile)
                elif args.resize:
                    resize_bitmap(afile)
                else:
                    converter(afile)
    else:
        for afile in glob.glob(fnpattern):
            if args.view_info:
                get_bitmap_info(afile)
            elif args.resize:
                resize_bitmap(afile)
            else:
                converter(afile)

if args.resize:
    print('%d file(s) have been resized.' %(cnt))
elif not args.view_info:
    print('%d file(s) have been converted.' %(cnt))