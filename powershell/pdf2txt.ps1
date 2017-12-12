$pdf = $args[0]
if (!($pdf)) {write-output "Usage: pdf2txt.ps1 foo.pdf"; break}
if (!(test-path($pdf))) {write-output "$pdf does not exist.";break}
$ext = (get-item $pdf).extension
$path = (get-item $pdf).fullname
if ($ext -ne ".pdf") {write-output "Specify a pdf file."}
else {pdftotext -nopgbrk -raw -enc UTF-8 $path}