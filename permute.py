import argparse

parser = argparse.ArgumentParser(
    description = 'Permute letters.'
)
parser.add_argument(
    'letters',
    type = str,
    nargs = 1,
    help = 'Type letters.'
)
parser.add_argument(
    '-r',
    dest = 'row',
    action = 'store_true',
    default = False,
    help = 'Show results in a row.'
)
parser.add_argument(
    '-n',
    dest = 'number',
    action = 'store_true',
    default = False,
    help = 'Show results with number.'
)
parser.add_argument(
    '-s',
    dest = 'sort',
    action = 'store_true',
    default = False,
    help = 'Sort letters before permuting.'
)
args = parser.parse_args()
# letters = args.letters[0].split(" ")
letters = list(args.letters[0])

num = 0
row = []

def permute(a, k=0):    
    global num
    global row
    if k == len(a):
        result = ''.join(a)
        if args.row:
            if args.number:
                num = num + 1                
                row.append('[%d]%s' %(num, result))
            else:
                row.append(result)
        else:
            if args.number:
                num = num + 1
                print('%6d: %s' %(num, result))
            else:
                print(result)
    else:        
        for i in range(k, len(a)):            
            a[k], a[i] = a[i] ,a[k]
            permute(a, k+1)
            a[k], a[i] = a[i], a[k]

if args.sort:
    letters.sort()
permute(letters)
if args.row:
    print(' '.join(row))