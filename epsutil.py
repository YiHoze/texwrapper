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
    description = 'Convert EPS, PDF, SVG images to other vector or bitmat formats. This script requires TeX Live, Inkscape, and ImageMagick. Be aware that SVG cannot be the target format. (eps/pdf/svg to pdf/eps/jpg/png)'  
)
parser.add_argument(
    'image',
    nargs = '+',
    help = 'Specify one or more vector images.'
)
parser.add_argument(
    '-t',
    dest = 'target_format',
    default = 'pdf',
    help = 'Specify the target format. (default: pdf)'
)
parser.add_argument(
    '-d',
    dest = 'density',
    type = int,
    default = 200,
    help = 'pixel density (default: 200 pixels per centimeter)'
)
parser.add_argument(
    '-r',
    dest = 'recursive',
    action = 'store_true',
    default = False,
    help = 'process ones in all subdirectories'
)
args = parser.parse_args()

def if_TeXLive_exists():
    try:
        subprocess.check_call('epstopdf.exe --version')
    except OSError:
        print("Make sure TeX Live is included in PATH.")
        sys.exit()

def if_Inkscape_exists():
    try:
        cmd = InkscapePath + ' --version'
        subprocess.check_call(cmd)
    except OSError:
        print("Check the path to Inkscape.")
        sys.exit()

def if_Imagemagick_exists():
    try:
        cmd = MagickPath + ' --version'
        subprocess.check_call(cmd)
    except OSError:
        print("Check the path to ImageMagick.")
        sys.exit()

def check_converter(fnpattern):
    srcfmt = os.path.splitext(fnpattern)[1]
    srcfmt = srcfmt.lower()
    if trgfmt == '.png' or trgfmt == '.jpg':
        if_Imagemagick_exists()
    elif srcfmt == '.svg':
        if_Inkscape_exists()
    else:
        if_TeXLive_exists()

def eps_to_pdf(src):
    global cnt
    os.system('epstopdf.exe %s' %(src))
    cnt += 1
    #print('%s: %d' %(src,cnt))

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

def vector_to_bitmap(src, trg):
    global cnt
    cmd = '\"%s\" -units PixelsPerCentimeter -density %d %s %s' %(MagickPath, args.density, src, trg)
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

trgfmt = args.target_format
trgfmt = trgfmt.lower()
if not trgfmt.startswith('.'):
    trgfmt = '.' + trgfmt

cnt = 0
for fnpattern in args.image: 
    check_converter(fnpattern)   
    if args.recursive:
        filename = os.path.basename(fnpattern)        
        subdirs = get_subdirs(fnpattern)
        for subdir in subdirs:
            subfile = os.path.join(subdir, filename)
            for afile in glob.glob(subfile):
                converter(afile)
    else:
        for afile in glob.glob(fnpattern):
            converter(afile)
print('%d file(s) have been converted.' %(cnt))