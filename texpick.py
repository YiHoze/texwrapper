import os, sys, glob, argparse, re

parser = argparse.ArgumentParser(
    description = 'Extract tex macros from a tex file.'
)
parser.add_argument(
    'tex',
    nargs = 1,
    help ='specify a tex file'
)
parser.add_argument(
    '-o',
    dest = 'output',
    default = None,
    help = 'specify a filename for output (default: foo_picked.txt)'
)
parser.add_argument(
    '-t',
    dest = 'tortoise',
    action = 'store_true',
    default = False,
    help = 'prepend the Tortoise Tagger syntax to the output for reference'
)
args = parser.parse_args()

if not os.path.exists(args.tex[0]):
    print('%s is not found' %(args.tex[0]))
    sys.exit()

if args.output is None:
    args.output = os.path.splitext(args.tex[0])[0] + '_picked.txt'

if os.path.exists(args.output):
    answer = input('%s alread exists. Are you sure to overwrite it? [y/N] ' %(args.output))
    if answer.lower() == 'y':
        os.remove(args.output)
    else:
        sys.exit()

reserved_patterns = [
    r'\\[^a-zA-Z]', 
    r'\\[a-zA-Z*^|+]+',
    r'\\begin(\{.+?\}[*^|+]*)', 
    r'(\w+=)'
]

with open(args.tex[0], mode='r', encoding='utf-8') as f:
    content = f.read()

# pick tex macros and keys
found = []
for i in range(len(reserved_patterns)):    
    p = re.compile(reserved_patterns[i])
    found += p.findall(content)
# remove duplicates and sort
found = set(found)
output = '\n'.join(sorted(found, key=str.lower))

tortoise = """
~~~FindAsIs
~~~WriteAsIs
~~~WC-OFF
\이 이
\가 가
\을 을
\를 를
\은 은
\는 는
\와 와
\과 과
\로 로
\으로 으로
\라 라
\이라 이라
~~~FindAsIs
~~~WriteInternal
~~~WC-ON
~~~FindAsIs
~~~WriteInternal
~~~WC-OFF
{
}
[
]
&
"""
if args.tortoise:
    output = tortoise + output

with open(args.output, mode='w', encoding='euc-kr') as f:
    f.write(output)

os.system('open.exe %s' %(args.output))
