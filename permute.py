import argparse

parser = argparse.ArgumentParser(
    description = 'Permute letters.'
)
parser.add_argument(
    'letters',
    type = str,
    nargs = 1,
    help = 'Type letters with space.'
)
parser.add_argument(
    '-c',
    dest = 'count',
    action = 'store_true',
    default = False,
    help = 'Count the number of mutations.'
)
args = parser.parse_args()
letters = args.letters[0].split(" ")

cnt = 0
def perm(a, k=0):    
    global cnt
    if k == len(a):
        str = ''.join(a)
        cnt = cnt + 1
        if args.count:
            print(str, cnt)
        else:
            print(str)
    else:        
        for i in range(k, len(a)):            
            a[k], a[i] = a[i] ,a[k]
            perm(a, k+1)
            a[k], a[i] = a[i], a[k]

perm(letters)
