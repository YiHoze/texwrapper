# pip install pyspellchecker
import os
import sys
import argparse
import glob
import re
from spellchecker import SpellChecker
from wordig import WordDigger


def parse_args():
    
    parser=argparse.ArgumentParser(
            description='English spell checker, particularly for LaTeX documentation'
        )
    parser.add_argument(
            'filters',
            nargs='+',
            help='Specify one or more tex files.'
        )
    parser.add_argument(
            '-s',
            dest='strip',
            action='store_false',
            default=True,
            help='Do not strip tex macros.'
        )
    parser.add_argument(
            '-r',
            dest='regex',
            default='detex.tsv',
            help='Specify a regex file in TSV format to remove markup.'
        )
    parser.add_argument(
            '-I',
            dest='ignore',
            default='ignore_words.txt',
            help='Specify a file that contains words to be ignored.'
        )

    return parser.parse_args()

def name_output(filename:str) -> str:

    filename, ext = os.path.splitext(os.path.basename(filename))

    return f"{filename}_stripped{ext}", f"{filename}_misspelt{ext}"


def find_misspelt(filename:str):
    
    intermediary, result = name_output(filename)
    if args.strip:
        WordDigger([filename], pattern=args.regex, output=intermediary, overwrite=True)
        filename = intermediary

    with open(filename, mode="r", encoding="utf-8") as fs:
        content = fs.readlines()

    misspelt = []
    for line in content:
        text = re.sub('[\.\,\:\`\'\"\(\)\-\/]', ' ', line)
        words = text.split()
        found = list(spell.unknown(words))
        if len(found) > 0:
            misspelt += found

    if len(misspelt) > 0:
        with open(result, mode='w', encoding='utf-8') as fs:
            fs.write('\n'.join(misspelt))


args = parse_args()
spell = SpellChecker(language='en')

if os.path.exists(args.ignore):
    with open(args.ignore, mode='r', encoding='utf-8') as fs:
        content = fs.read()
        words = content.split()
        spell.word_frequency.load_words(words)

if args.strip:
    if not os.path.exists(args.regex):
        tmp = os.path.join(os.path.dirname(__file__), args.regex)
        if os.path.exists(tmp):
            args.regex = tmp
        else:
            print(f"{tmp} is not found.")
            sys.exit()

for filter in args.filters:
    for file in glob.glob(filter):
        find_misspelt(file)