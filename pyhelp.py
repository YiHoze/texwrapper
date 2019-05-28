import sys
import argparse

if sys.version_info.major < 3 and sys.version_info.minor < 4:
    from imp import import_module
else:
    from importlib import import_module

parser = argparse.ArgumentParser(
    description = 'Get help for a python component.'
)
parser.add_argument(
    'component',
    type = str,
    help = 'Type what you want to learn about.'
)
parser.add_argument(
    '-m',
    dest = 'module',
    help = 'Type a module to import.'

)
args = parser.parse_args()

if args.module is not None:
    import_module(args.module)

help(args.component)
