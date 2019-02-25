# git init
# git add README.md
# git commit -m "first commit"
# git remote add origin https://github.com/YiHoze/foo.git
# git push -u origin master

import os, sys, argparse, configparser
import datetime

try:
    inipath = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    inipath = False
if inipath is False:
    inipath = os.path.dirname(sys.argv[0])
ini = os.path.join(inipath, 'gitpush.ini')
if not os.path.exists(ini):
    print('gitpush.ini is not found. Set the DOCENV environment variable to the directory containing daily.ini.')
    sys.exit()

repository_list = []
config = configparser.ConfigParser()
config.read(ini)
for section in config.sections():
    repository_map = {}
    for key in config[section]:
        repository_map[key] = config.get(section, key)
    repository_list.append(repository_map)
#print(repository_list)

parser = argparse.ArgumentParser(
    description = 'Commit and push file changes to your remote Git repository'
)
parser.add_argument(
    'repository',
    nargs = '*',
    help = 'specify one or more repository aliases'
)
parser.add_argument(
    '-c',
    dest = 'commit_message',
    default = None,
    help = 'Type a commit message (default: date_time)'
)
args = parser.parse_args()

if args.commit_message is None:
    now = datetime.datetime.now()    
    args.commit_message = now.strftime("%Y-%m-%d_%H:%M")

def show_repository_aliases():
    print('Available repositories are:')
    for i in range(len(repository_list)):
        print('%-10s %s' %(repository_list[i]['alias'], repository_list[i]['local']))
    sys.exit()

if not bool(args.repository):
   show_repository_aliases()

repository_aliases = [repository_list[i]['alias'] for i in range(len(repository_list))]

for alias in args.repository:
    try:
        index = repository_aliases.index(alias)
        os.chdir(repository_list[index]['local'])
        os.system('git add *')
        os.system('git commit -m "%s"' %(args.commit_message))        
        os.system('git push origin master')
    except:
        show_repository_aliases()

