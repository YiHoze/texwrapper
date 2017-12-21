import os, sys, argparse
import re

# Get arguments
parser = argparse.ArgumentParser(
    description = 'Bookmark index entries'
)
parser.add_argument(
    'ind',
    type = str,
    nargs = 1,
    help = 'Specify an index file.'
)
parser.add_argument(
    '-p',
    dest = 'BookmarkPython',
    action = 'store_true',
    default = False,
    help = 'Bookmark index entries which are Python functions extracted from docstrings.'
)
args = parser.parse_args()
indfile = args.ind[0]

if not os.path.exists(indfile):
    print('%s is not found' % (indfile))
    sys.exit()

tmp = 't@mp.t@mp'
if os.path.exists(tmp):
    os.remove(tmp)

def bookmark_index(line, pattern):
    entry = re.search(pattern, line)
    if entry: 
        page = re.findall('\\\\hyperpage\\{(\\d+)\\}', line)
        append = ''
        for i in range(len(page)):
            append += '\t\\bookmark[level=2, page=%s]{%s}\n' %(page[i], entry.group(1))                    
        line += append
    return(line)
    
with open(tmp, mode='w', encoding='utf-8') as new_file, open(indfile, mode='r', encoding='utf-8') as old_file:
    if args.BookmarkPython:
        for line in old_file.readlines():
            new_file.write(bookmark_index(line, '\\\\item (.+?)\\(\\)'))
    else:
        for line in old_file.readlines():
            new_file.write(bookmark_index(line, '\\\\item (.+?),'))
            
os.remove(indfile)
os.rename(tmp, indfile)