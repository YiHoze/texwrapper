import  os, argparse

parser = argparse.ArgumentParser(
    description = 'Get help for a python component.'
)
parser.add_argument(
    'component',
    type = str,
    nargs = 1,
    help = 'Type what you want to learn about.'
)
parser.add_argument(
    '-m',
    dest = 'module',
    help = 'Type a module to import.'

)
args = parser.parse_args()

tmppy = args.component[0] + "tmp.py"

content = ''
if args.module is not None:
    content = 'import %s\n' %(args.module)
content += 'help(%s)' %(args.component[0])

with open(tmppy, mode='w') as f:
    f.write(content)
os.system(tmppy)
os.remove(tmppy)