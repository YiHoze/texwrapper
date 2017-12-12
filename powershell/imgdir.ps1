$directory = $args[0]
if (!($directory)) {$directory = "."}
if (!(Test-Path($directory))) {Write-Output "$directory does not exist."; break}

$file = $args[1]
if (!($file)) {$file = "imgdir.txt"}
if (Test-Path($file)) {	Remove-Item $file}

$ImageTypes = @("pdf", "jpg", "png")
foreach ($element in $ImageTypes) {
	Get-ChildItem -path $directory "*.$element" -name | Add-Content $file -Encoding UTF8
}
