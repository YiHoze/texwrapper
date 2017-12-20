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

ini = os.path.split(sys.argv[0])[0]
if bool(ini):
    ini += '\daily.ini'
else: # in case this source code is called by Python when the terminal's current directory is that which contains this script.
    ini = 'daily.ini'
config = configparser.ConfigParser()

if os.path.exists(ini):    
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
        cmd = '\"%s\" %s' % (app, target.replace('\n', ' '))
        subprocess.Popen(cmd)        
else:
    input('daily.ini is not found. Press any key to exit.')
    