[CmdletBinding()]
param(
  [string] $files,
  [alias('o')][string] $output,
  [alias('h')][switch] $help
)

function help
{
  write-output "
  filemerge.ps1 *.txt [-o output.txt]
    default output: m@rged.txt
  "
  break
}

if (!$files -or $help) { help; break }

if ( !(test-path($files)) ) {
  write-output "$files do not exist."
  break
}

if (!$output) { $output = "m@rged.txt" }
if (test-path($output)) { remove-item $output }

foreach ($file in get-childitem $files -file) {
  $content = get-content $file -encoding UTF8 #-ReadCount 0
  add-content $output -value $content -encoding UTF8
}
