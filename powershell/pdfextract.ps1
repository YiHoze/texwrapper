$file = $args[0]
$page = $args[1]

if (!($file)) {write-Output "Usage: extractpdf.ps1 foo.pdf 10 (page number)"; break}
if (!(test-path($file))) {write-output "$file does not exist.";break}

if (!($page)) {
	$answer = read-host "Do you want to extract all pages? (Enter Y or N)"
	if (($answer -eq 'y') -or ($answer -eq 'Y')) {		
		$output = (get-item $file).basename + "_%d.pdf"
		$paras = @($file, "burst", "output", $output)		
	} else {	
		$output = (get-item $file).basename + "_" + $page + ".pdf"
		$paras = @($file, "cat", $page, "output", $output)
	}
}

&"C:\Program Files (x86)\PDFtk\bin\Pdftk.exe" $paras

$answer = read-host "Do you want to convert extracted pages to PNG? (Enter Y or N)"
if (($answer -eq 'y') -or ($answer -eq 'Y')) {
	$output = (get-item $file).basename + "_*.pdf"
	vec2bit.ps1 $output
}
