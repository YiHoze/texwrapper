[CmdletBinding()] 
param(
  [alias("s")][string] $scale="1",
  [alias("n")][string] $job="album",  
  [alias("h")][switch] $help=$false
)

function help{
write-output "
makealbum.ps1 [options]
  -s: image scale (1 by default) 
  -f: album filename (`"album`" by default)
  -h: help
"
}

if ($help) { help; break }

$tex = $job + ".tex"
$dir = $job + ".txt"
$pdf = $job + ".pdf"

if (Test-Path($pdf)) {
Write-Output "$pdf already exists."
$answer = Read-Host "Do you want to overwrite it? (Enter Y or N)"
  if (($answer -eq 'y') -or ($answer -eq 'Y')) {
    remove-item $pdf -force
    if (Test-Path($dir)) { remove-item $dir }    
  } else {
    break
  }
}

$ImageTypes = @("pdf", "jpg", "png")
foreach ($element in $ImageTypes) {
  Get-ChildItem "*.$element" -name | Add-Content $dir -Encoding UTF8
}

$src = "\documentclass{hzguide}
%%\usepackage{multicol}
\LayoutSetup{paper=A4}
\HeadingSetup{type=report}
\begin{document}
%%\begin{multicols}{2}
\MakeAlbum[$scale]{$dir}
%%\end{multicols}
\end{document}"

Set-Content $tex -Encoding UTF8 $src
xelatex $tex
texclean.ps1
#Remove-Item $dir
#Remove-Item $tex
