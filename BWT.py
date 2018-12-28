import os, argparse
from itertools import permutations
from nltk.corpus import wordnet
parser = argparse.ArgumentParser(
    description = 'Permute letters to beat the WORD TOWER mobile game.'
)
parser.add_argument(
    'letters',
    type = str,
    nargs = 1,
    help = 'Type letters without space.'
)
parser.add_argument(
    'quantity',
    type = int,
    nargs = '?',
    default = 0,
    help = """Specify how many letters to use among the given letters for permutation. 
    The default is the count of the given letters."""
)
parser.add_argument(
    '-c',
    dest = 'column',
    type = int,
    default = 10,
    help = 'Specify the number of columns in which the list of permuted words is displayed.'
)
args = parser.parse_args()
letters = list(args.letters[0])

if args.quantity == 0:
    args.quantity = len(letters)
    partial = False
else:
    partial = True

perm = permutations(letters, args.quantity)
results = []
for i in list(perm):
    result = ''.join(i)
    if wordnet.synsets(result):
        results.append(result)
results = list(set(results))
results.sort()

i = 0
lines = ''
while i < len(results):
    for j in range(args.column):
        k = i + j
        if k < len(results):
            lines += '%-12s' %(results[k])
        else:
            break
    lines += '\n'
    i += args.column
    
if partial is True:
    if os.path.exists('t@mp.txt'):
        os.remove('t@mp.txt')
    with open('t@mp.txt', mode = 'w') as f:
        f.write(lines)
    os.system('powershell -command open.py t@mp.txt')
else:
    print(lines)