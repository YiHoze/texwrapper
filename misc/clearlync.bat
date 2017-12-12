taskkill /im lync.exe
taskkill /im outlook.exe
TIMEOUT 2
cd %appdata%\microsoft\office\16.0
rename lync lync.old
cd %localappdata%\microsoft\office\16.0
rename lync lync.old
