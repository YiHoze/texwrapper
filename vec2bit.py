import os, sys, glob, argparse, subprocess

parser = argparse.ArgumentParser(
    description = 'Convert vector images to bitmap using Ghostscript'
)
parser.add_argument(
    'image',
    nargs = '+',
    help = 'specify one or more eps or pdf images'
)
parser.add_argument(
    '-f',
    dest = 'target_format',
    default = 'png',
    help = 'specify a target format: jpg, png (default: png)'
)
parser.add_argument(
    '-r',
    dest = 'resolution',
    default = 254,
    help = 'specify a resolution (default: 254 ppi)'
)
args = parser.parse_args()

try:
    cmd = 'gswin64c -v'
    subprocess.check_call(cmd)    
except OSError:
    print('Make sure that the Ghostscript directory (gswin64c.exe) is included in the PATH environment variable.')
    sys.exit()

if args.target_format is 'jpg':
    device = 'jpeg'
else:
    device = 'pngalpha'

cmd = '-dBATCH -dNOPAUSE -sDEVICE=%s -r%s -dEPSCrop ' %(device, args.resolution)

for fnpattern in args.image:
    for afile in glob.glob(fnpattern):
        #output = os.path.basename(afile) + '.' + args.target_format
        output = os.path.splitext(afile)[0] + '.' + args.target_format
        cmd = 'gswin64c -dBATCH -dNOPAUSE -sDEVICE=%s -r%s -dEPSCrop -sOutputFile=%s %s' %(device, args.resolution, output, afile)        
        os.system(cmd)