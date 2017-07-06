$doc = $args[0]
if (!($doc)) {write-output "Usage: doc2txt.ps1 foo.doc"; break}
if (!(test-path($doc))) {write-output "$doc does not exist.";break}
$ext = (get-item $doc).extension
$path = (get-item $doc).fullname
switch ($ext) {
	".docx" {doc2.vbs $path docx txt}
	".doc" {doc2.vbs $path doc txt}
	default {write-output "Specify a doc or docx file."}
}