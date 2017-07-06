if (!($args[0])) { 
  write-output "imgconvert.ps1 *.jpg png"
  break
}

$files = $args[0]
$trgext = $args[1]

foreach ($element in get-childitem $files -name) {
	$target = (get-item $element).basename + "." + $trgext
	magick $element $target
}