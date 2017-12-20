import os, glob, argparse, subprocess

parser = argparse.ArgumentParser(
    description='Count words in a text file. This program can process PDF files if TeX Live is installed.'
)
parser.add_argument(
    'files',
    type=str,
    nargs='+',
    help='Specify files to count their words.'
)
args = parser.parse_args()

try:
    cmd = 'pdftotext -v'
    subprocess.check_call(cmd)
    pdftotext = True
except OSError:
    print('pdftotext.exe is not found, so PDF files cannot be processed.')
    pdftotext = False

# Spaces are not counted as a character.
def count_words(afile):
    lines, chars, words = 0, 0, 0
    f = open(afile, mode='r', encoding='utf-8')
    for line in f.readlines():
        lines += 1
        chars += len(line.replace(' ', '')) 
        this = line.split(None)
        words += len(this)
    f.close()
    msg = '%s\n Lines: %d\n Words: %d\n Characters: %d\n' % (afile, lines, words, chars)
    print(msg)    

for fnpattern in args.files:
    for afile in glob.glob(fnpattern):
        filename, ext = os.path.splitext(afile)
        if ext.lower() == '.pdf':
            if pdftotext:
                cmd = 'pdftotext -nopgbrk -raw -enc UTF-8 %s' % (afile)
                os.system(cmd)
                file = filename + '.txt'
            else:
                continue
        count_words(afile)
        