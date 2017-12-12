$file=$Args[0]
if (!($file)) {Write-Output "Convert EPS to PDF: e2p foo(.eps) or *(.eps)"; break}

if ($file.Contains('*')) {
	if (!($file.EndsWith(".eps"))) {$file = $file + ".eps"}
	foreach ($this in Get-ChildItem $file -name) {epstopdf $this}
break
} else {
	if (!($file.EndsWith(".eps"))) {$file = $file + ".eps"}
	if (!(Test-Path($file))) {Write-Output "$file does not exist."; break}
	else {epstopdf $file}
}
#for %%i in (*.eps) do gswin32c -sDEVICE=pdfwrite -dEPSCrop -o %%~ni.pdf %%i