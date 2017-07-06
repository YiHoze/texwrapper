$file=$Args[0]
if (!($file)) {Write-Output "pdf2eps foo.pdf"; break}

if ($file.Contains('*')) {
  if (!($file.EndsWith(".pdf"))) {$file = $file + ".eps"}
  foreach ($this in Get-ChildItem $file -name) {pdftops $this -eps}
  break
} else {
  if (!($file.EndsWith(".pdf"))) {$file = $file + ".pdf"}
  if (!(Test-Path($file))) {Write-Output "$file does not exist."; break}
  else {pdftops $file -eps}
}