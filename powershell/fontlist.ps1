$file = "FontsList.txt"
if (test-path $file) { remove-item $file }
fc-list -f "%{family}\n" >> $file
Get-Content $file | sort -Unique | set-content $file -encoding UTF8
open.ps1 $file 