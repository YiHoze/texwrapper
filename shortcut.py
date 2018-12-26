import os, sys, glob, argparse, winshell
from win32com.client import Dispatch

parser = argparse.ArgumentParser(
    description = 'Create a shortcut into a favorite or specific directory.'
)
parser.add_argument(
    'files',
    nargs = '+',
    help = 'Specify a file or more to create their shortcuts.'
)
parser.add_argument(
    '-d',
    dest = 'destination_path',
    default = r'C:\Users\Hoze\Favorites\링크',
    help = r'Specify the destination directory. The default path is C:\Users\Hoze\Favorites\링크.'
)
args = parser.parse_args()

shell = Dispatch('WScript.Shell')
for fnpattern in args.files:
    for afile in glob.glob(fnpattern):
        target_path = os.path.abspath(afile)
        filename = os.path.basename(afile) + '.lnk'
        shortcut_path = os.path.join(args.destination_path, filename)
        # print(target_path, shortcut_path)
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        # shortcut.WorkingDirectory = os.path.dirname(target_path)
        # shortcut.IconLocation = target_path
        shortcut.save()