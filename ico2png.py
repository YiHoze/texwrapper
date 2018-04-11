import os, sys, glob, argparse, subprocess

parser = argparse.ArgumentParser(
    description='Convert .ico files to PNG or JPG.'
)
parser.add_argument(
    'icons',
    metavar = 'icon file',
    nargs = '+',
    help = 'specify one or more .ico files.'    
)
parser.add_argument(
    '-f',
    dest = 'target_format',
    default = 'png',
    help = 'specify what format images should be converted to. (default: png)'
)
args = parser.parse_args()

# Check if ImageMagick is accessible.
try:
    cmd = 'magick.exe -version'
    subprocess.check_call(cmd)    
except OSError:
    print("Make sure that ImageMagick is included in the PATH environment variable.")
    exit(False)

for fnpattern in args.icons:
    for afile in glob.glob(fnpattern):
        filename = os.path.splitext(afile)
        trg = filename[0] + '.' + args.target_format
        cmd = 'magick.exe %s %s' %(afile, trg)
        os.system(cmd)