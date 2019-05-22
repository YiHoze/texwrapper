import argparse, re, os

parser = argparse.ArgumentParser(
    description = 'Repeat a command to process multiple files that contain serial numbers.'
)
parser.add_argument(
    'command',
    type = str,
    nargs = 1,
    help = 'Type a command in quotation marks.'
)
parser.add_argument(
    'upto',
    type = int,
    nargs = 1,
    help = 'Specify the end number.'
)
parser.add_argument(
    '-s',
    dest = 'start',
    default = 1,
    help = 'Specify the start number.'
)
parser.add_argument(
    '-n',
    dest = 'noleading',
    action = 'store_true',
    default = False,
    help = 'Do not add a leading zero to single-digit numbers.'
)
args = parser.parse_args()

cnt = args.start
while cnt <= args.upto[0]:
    if args.noleading:
        cntstr = str(cnt)
    else:
        cntstr = "{:02d}".format(cnt)
    cmd = re.sub('\*', cntstr, args.command[0])
    # print(cmd)
    os.system(cmd)
    cnt += 1