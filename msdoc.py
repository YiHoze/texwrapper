import os, sys, glob, argparse

try:
    dir_called = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    dir_called = False
if dir_called is False:
    dir_called = os.path.dirname(sys.argv[0])
vbs = os.path.join(dir_called, 'msdoc.vbs')

if not os.path.exists(vbs):
    print('%s is not found.' %(vbs))
    sys.exit()

parser = argparse.ArgumentParser(
    description = 'Convert a file to another format using Microsoft Word.'
)
parser.add_argument(
    'doc',
    nargs = '+',
    help = 'specify one or more document files'
)
parser.add_argument(
    '-f',
    dest = 'target_format',
    default = 'pdf',
    help = 'specify a target format: doc, docx, html, rtf, txt, pdf, xml (default: pdf)'
)
args = parser.parse_args()

for fnpattern in args.doc:
    for doc in glob.glob(fnpattern):
        source_path = os.path.realpath(doc)
        source_format = os.path.splitext(doc)[1][1:]
        os.system('%s %s %s %s' %(vbs, source_path, source_format, args.target_format))
