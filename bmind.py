import os, sys, argparse
import re

# Get arguments
parser = argparse.ArgumentParser(
    description = 'Bookmark index entries which are Python functions extracted from docstrings.'
)
parser.add_argument(
    'ind',
    type = str,
    nargs = 1,
    help = 'Specify an index file.'
)
args = parser.parse_args()
file = args.ind[0]

if not os.path.exists(file):
    msg = '%s is not found' % (file)
    print(msg)
    sys.exit()

tmp = 't@mp.t@mp'
if os.path.exists(tmp):
    os.remove(tmp)

with open(tmp, mode='w', encoding='utf-8') as new_file, open(file, mode='r', encoding='utf-8') as old_file:
    for line in old_file.readlines():
        func = re.search('\\\\item (.+?)\\(\\)', line)
        if func: 
            page = re.search('\\\\hyperpage\\{(\\d+)\\}', line)
            #print(func.group(1), page.group(1))
            line = '%s\\bookmark[level=2, page=%s]{%s}\n' % (line.replace('\n', ''), page.group(1), func.group(1))
        new_file.write(line)
os.remove(file)
os.rename(tmp, file)