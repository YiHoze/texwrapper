[CmdletBinding()] 
param(
  [string] $files,
  [alias("t")][string] $type="png",
  [alias("s")][string] $resolution="254",  
  [alias("h")][switch] $help=$false
)

function help{
write-output "
vec2bit.ps1 files [options] 
  -t: bitmap type (png by default) 
  -r: resolution (250 ppi by default)
  -h: help
"
}

if ($help -or !$files) { help; break }

if ( !($files.EndsWith(".pdf")) -and !($files.EndsWith(".eps")) ) {
  write-output "Specify PDF or EPS files"
  break
}

switch ($type) {
	"jpg" {$device="jpeg"}
	"png" {$device="pngalpha"}
}

$paras = @("-dBATCH", "-dNOPAUSE", "-sDEVICE=$device", "-r$resolution", "-dEPSCrop", "", "")

foreach ($file in get-childitem $files -file) {
  $paras[5] = "-sOutputFile=" + $file.basename + "." + $type
  $paras[6] = $file
  gswin64c $paras
}
