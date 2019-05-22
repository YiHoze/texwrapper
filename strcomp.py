import os, sys, argparse, csv
from difflib import SequenceMatcher

parser = argparse.ArgumentParser(
    description = 'Get the match rate between two strings.'
)
parser.add_argument(
    'strings',
    nargs = '*',
    help = 'Type two strings wrapped with quotation marks, or Specify a TSV file that contains strings in two columns.'
)
args = parser.parse_args()

def ProcessTSV():
    lines = 0
    matches = 0
    filename = os.path.basename(args.strings[0])
    basename = os.path.splitext(filename)[0]
    infile = basename + '.tsv'
    outfile = basename + '_result.tsv'    
    if not os.path.exists(infile):
        print("%s does not exist." %(infile))
        return
    with open(infile, mode='r', encoding='utf-8') as source, open(outfile, mode='w', encoding='utf-8') as result:
        reader = csv.reader(source, delimiter='\t')
        writer = csv.writer(result, delimiter='\t', lineterminator='\n')
        for line in reader:
            s = SequenceMatcher(None, line[0], line[1])
            lines += 1
            match = "{0:.1f}%".format(s.ratio() * 100)
            matches += s.ratio()
            writer.writerow([line[0], line[1], match])
        matches = matches / lines
        average = "Average match rate: {0:.1f}%".format(matches * 100)
        print(average)
        writer.writerow([average])

if len(args.strings) == 0:
    parser.print_help()
elif len(args.strings) == 1:
    ProcessTSV()
else:
    s = SequenceMatcher(None, args.strings[0], args.strings[1])
    print("{0:.1f}%".format(s.ratio() * 100))
