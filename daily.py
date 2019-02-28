# [Chrome]
# app = C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
# target =     
#     http://dic.daum.net/index.do?dic=eng 
#     http://www.ktug.org

import os, sys, argparse, configparser, subprocess 

parser = argparse.ArgumentParser(
    description = 'Open apps and their targets specified in daily.ini.'
)
parser.add_argument(
    'list',
    nargs = '?',
    help = 'Specify another daily to-do list.'
)
args = parser.parse_args()

if args.list is None:
    try:
        inipath = os.environ['DOCENV'].split(os.pathsep)[0]
    except:
        inipath = False
    if inipath is False:
        inipath = os.path.dirname(sys.argv[0])
    ini = os.path.join(inipath, 'daily.ini')
else:
    ini = args.list

if os.path.exists(ini):
    config = configparser.ConfigParser()
    with open(ini, mode='r', encoding='utf-8') as f:
        config.readfp(f)
    for section in config.sections():
        try:
            app = config.get(section, 'app')
        except:
            app = ''
        try: 
            target = config.get(section, 'target')
        except:
            target = ''
        cmd = '\"%s\" %s' %(app, target.replace('\n', ' '))
        # cmd.encode(encoding='euc-kr')
        subprocess.Popen(cmd)        
else:
    print('%s is not found.' %(ini))