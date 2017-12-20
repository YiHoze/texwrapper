import os, glob, argparse
import re
from itertools import product

parser = argparse.ArgumentParser(
    description = 'Replace 조사 with 자동 조사 such as \를'
)
parser.add_argument(
    'tex',
    nargs='+',
    help='Specify TeX files.'
)
args = parser.parse_args()

tags = [
    r'(\\ref\{.+?\})',    
    r'(\\eqref\{.+?\})',    
    r'(\\hyperref\[.+?\]\{\\.+?\}\})',
    r'(\\sphinxhref\{.+?\}\{.+?\})',
    r'(\\sphinxtitleref\{.+?\})'
]

josas = ['은', '는', '이', '가', '을', '를', '와', '과', '로', '으로', '라', '이라']

def josa_generator():
    for tag, josa in product(tags, josas):
        yield tag + josa, '\\1' + '\\\\' + josa

tmp = 't@mp.t@mp'
if os.path.exists(tmp):
    os.remove(tmp)

for files in args.tex:
    for afile in glob.glob(files):
        with open(afile, mode='r', encoding='utf-8') as f:
            content = f.read()        
        # for tag, josa in product(tags, josas):
        #     pattern = tag + josa
        #     subst = '\\1' + '\\\\' + josa
        for pattern, subst in josa_generator():
            content = re.sub(pattern, subst, content)
        with open(tmp, mode='w', encoding='utf-8') as f:
            f.write(content)        
        os.remove(afile)
        os.rename(tmp, afile)      
