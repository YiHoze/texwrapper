# count words in a pdf or text file
$file = $args[0]

if (!($file)) {write-output "wordcount.ps1 foo[.txt/pdf]"; break}
if (!(test-path($file))) {write-output "$file does not exist.";break}

if ((get-item $file).extension -eq ".pdf") {	
	#$path = (get-item $file).fullname
	pdftotext -nopgbrk -raw -enc UTF-8 $file
	$file = (get-item $file).basename + ".txt"
}

write-output "$file consists of:"
get-content $file | measure-object -line -word -character
