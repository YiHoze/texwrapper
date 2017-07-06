$file=$args[0]
if (!($file)) {Write-Output "Usage: pdfcrop *.pdf"; break}
$tmp = "@@@.pdf"

foreach ($this in get-childitem $file -name) {
  pdfcrop.exe $this $tmp
  remove-item $this 
  rename-item $tmp $this
}