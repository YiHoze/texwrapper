# dir s -r | % { if ($_.Name -cne $_.Name.ToLower()) { ren $_.FullName $_.Name.ToLower() } }
$option = $args[0]
$directory = $args[1]
if (!($option)) {$option = "-h"}
if (!($directory)) {$directory = "."}

function ToLowercase () {
get-childitem -file $directory | foreach-object {  ren $_.name $_.name.tolower() }
}

function ToUppercase () {
get-childitem -file $directory | foreach-object {  ren $_.name $_.name.toupper() }
}

switch ($option) {
	"-u" { ToUppercase }
	"-l" { ToLowercase }
	"-h" { write-output "Rename files to uppercase or lowercase.`nfilerecase.ps1 -u[-l] [.]" }
}
