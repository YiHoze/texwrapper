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
    p2t = True
except OSError:
    print('pdftotext.exe is not found, so PDF files cannot be processed.')
    p2t = False

# Spaces are not counted as a character.
def count_words(file):
    lines, chars, words = 0, 0, 0
    f = open(file, mode='r', encoding='utf-8')
    for line in f.readlines():
        lines += 1
        chars += len(line.replace(' ', '')) 
        this = line.split(None)
        words += len(this)
    f.close()
    msg = '%s\n Lines: %d\n Words: %d\n Characters: %d\n' % (file, lines, words, chars)
    print(msg)    

for pattern in args.files:
    for file in glob.glob(pattern):
        fn, ext = os.path.splitext(file)
        if ext.lower() == '.pdf':
            if p2t:
                cmd = 'pdftotext -nopgbrk -raw -enc UTF-8 %s' % (file)
                os.system(cmd)
                file = fn + '.txt'
            else:
                continue
        count_words(file)
        