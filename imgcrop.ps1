$file = $args[0]
$size = $args[1]

if ( !($file) ) { write-output "imgcrop.ps1 foo.png [1280x800+0+0]"; break }
if ( !($size) ) { $size = "1280x800+0+0" }

foreach ($element in get-childitem $file -name) {
	magick -crop $size $element $element
}