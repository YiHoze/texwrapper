# daily.ini:
# [App 1]
# app = C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
# target = 
#     https://login.microsoftonline.com 
#     http://dic.daum.net/index.do?dic=eng 
#     https://mail.google.com 
#     http://hoze.tistory.com 
#     http://www.ktug.org
# [App 2]
# app = C:\Program Files (x86)\FreeCommander XE\FreeCommander.exe
# [App 3]
# app = C:\Program Files\Microsoft VS Code\bin\code.cmd

import os, sys, configparser, subprocess
try:
    inipath = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    inipath = False
if inipath is False:
    inipath = os.path.dirname(sys.argv[0])
ini = os.path.join(inipath, 'daily.ini')
if os.path.exists(ini):    
    config = configparser.ConfigParser()
    config.read(ini)
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
        subprocess.Popen(cmd)
else:
    input('Daily.ini is not found. Set the DOCENV environment variable to the directory containing daily.ini. Press any key to exit.')