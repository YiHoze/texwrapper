# 1 inch = 2.54 cm
# 72 ppi = 28.346457 ppc
[CmdletBinding()]
param(
  [string] $files,
  [alias("r")][string] $resolution="100",
  [alias("s")][string] $scale="100",
  [alias("b")][switch] $backup=$false,
  [alias("h")][switch] $help=$false
)

function help {
write-output "
imgresize.ps1 [image_files] [options]
  -r: resolution (100 pixels per centimeter by default)
  -s: scale (100 % by default)
  -b: back up intended files
  -h: help
"
}

function displaycmd {
write-output "
 files: $files 
 resolution: $resolution
 scale: $scale
 backup: $backup
 help: $help
 "
}

if ($help -or !$files) { help; break }

foreach ($file in get-childitem $files -file -name) {
	if ($backup) {
		$bak = $file + ".bak"
		copy-item $file $bak -force
	}
	magick $file -units PixelsPerCentimeter -density $resolution -resize $scale% $file
}
