# Make a list that contains the names of all the fonts installed
$file = "FontsList.txt"
if(test-path($file)) {remove-item $file}
fc-list :outline -f "%{family}\n" >> $file
Get-Content $file -encoding UTF8 | sort-object | set-content $file -encoding UTF8
open.ps1 $file -t 