import os, sys, argparse

parser = argparse.ArgumentParser(
    description = 'View the list of installed fonts.'
)
parser.add_argument(
    '-o',
    dest = 'output',
    default = 'fontlist.txt',
    help = 'specify a file name for output (default: fontlist.txt)'
)
args = parser.parse_args()

if os.path.exists(args.output):
    os.remove(args.output)

os.system("fc-list : file >> %s" %(args.output))
with open(args.output, mode='r', encoding='utf-8') as f:
    content = f.readlines()
content.sort()
#content = ''.join(map(str, content))
with open(args.output, mode='w', encoding='utf-8') as f:
    for line in content:
        f.write(os.path.basename(line))
os.system("open.exe %s" %(args.output))
