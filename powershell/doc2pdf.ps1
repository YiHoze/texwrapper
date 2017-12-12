$doc = $args[0]
if (!($doc)) {write-output "Usage: doc2pdf.ps1 foo.doc"; break}

if ( $doc.contains('*') ) {
	$path = "."
	$ext = $doc.substring($doc.lastindexof("."), $doc.length-1)
} else {
	if (!(test-path($doc))) {write-output "$doc does not exist.";break}
	$path = (get-item $doc).fullname	
	$ext = (get-item $doc).extension
}

switch ($ext) {
	".docx" {doc2.vbs $path docx pdf}
	".doc" {doc2.vbs $path doc pdf}
	default {write-output "Specify a doc or docx file."}
}