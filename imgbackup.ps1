$destination = $args[0]
if (!($destination)) { 
	$destination = "./obsolete" 
} else { 
	if (!($destination.startswith("."))) { $destination = "./" + $destination } 
}

if (!(test-path($destination))) {
	$answer = read-host "Do you want to create $destination folder? (Enter Y or N)"
	if (($answer -eq 'y') -or ($answer -eq 'Y')) {
		new-item -itemtype directory -path $destination
	} else {	
		break
	}
}

Function RemovePNG ($file) {
	$file = $file + ".png"	
	if (test-path($file)) { move-item -path $file $destination -force}
}

Function RemoveJPG ($file) {
	$file = $file + ".jpg"	
	if (test-path($file)) { move-item -path $file $destination -force }
}

$epslist = get-childitem "*.eps" -name 2>&1

foreach ($element in $epslist) {
	$target = (get-item $element).basename
	RemovePNG($target)
	RemoveJPG($target)
}

$epslist = get-childitem "*.pdf" -name 2>&1

foreach ($element in $epslist) {
	$target = (get-item $element).basename
	RemovePNG($target)
	RemoveJPG($target)
}
